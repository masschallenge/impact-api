# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from random import shuffle
from accelerator.models import (
    ACTIVE_PANEL_STATUS,
    Allocator,
    Application,
    ApplicationPanelAssignment,
    ASSIGNED_PANEL_ASSIGNMENT_STATUS,
    JudgeApplicationFeedback,
    JudgePanelAssignment,
    JudgingRound,
    Panel,
    Scenario,
    User,
)
from rest_framework.response import Response
from impact.v1.views.impact_view import ImpactView
from impact.v1.classes.allocate_applications_permissions import (
    AllocateApplicationsPermissions,
)

ALREADY_ASSIGNED_ERROR = "{judge} is already assigned to {count} applications"
JUDGING_ROUND_INACTIVE_ERROR = "Judging round {} is not active"
NO_APP_LEFT_FOR_JUDGE = "{} has provided feedback on all applications"


class AllocateApplicationsView(ImpactView):
    permission_classes = (
        AllocateApplicationsPermissions,
    )
    view_name = "allocate_applications"

    def __init__(self):
        self.errors = []

    def get(self, request, round_id, judge_id):
        self.judging_round = JudgingRound.objects.get(pk=round_id)
        self.judge = User.objects.get(pk=judge_id)
        self.scenario = self._find_scenario()
        self._validate()
        if self.errors:
            return self._failure()
        applications = self._allocate()
        if self.errors:
            return self._failure()
        return Response(applications)

    def _validate(self):
        self._check_judging_round()
        self._check_assignments()

    def _check_judging_round(self):
        if not self.judging_round.is_active:
            self.errors.append(JUDGING_ROUND_INACTIVE_ERROR.format(
                self.judging_round.id))

    def _check_assignments(self):
        count = JudgePanelAssignment.objects.filter(
            scenario=self.scenario,
            judge=self.judge,
            assignment_status=ASSIGNED_PANEL_ASSIGNMENT_STATUS).count()
        if count > 0:
            self.errors.append(ALREADY_ASSIGNED_ERROR.format(
                judge=self.judge.email, count=count))

    def _allocate(self):
        choices = self._find_app_id_choices()
        if not choices:
            self.errors.append(NO_APP_LEFT_FOR_JUDGE.format(self.judge.email))
        else:
            shuffle(choices)
            count = min(len(choices), self.scenario.panel_size)
            result = choices[:count]
            self._make_panel(result)
            return result
        return []

    def _find_app_id_choices(self):
        judging_round = self.judging_round
        app_ids = set(Application.objects.filter(
            application_type=judging_round.application_type,
            application_status="submitted").values_list("id", flat=True))
        judge_app_ids = set(JudgeApplicationFeedback.objects.filter(
            panel__judgepanelassignment__scenario__judging_round=judging_round,
            judge=self.judge).values_list("application_id", flat=True))
        return list(app_ids - judge_app_ids)

    def _enable_additional_assignments(self, desired):
        goal = self._judge_assignment_count() + desired
        commitment = self.judge.judgeroundcommitment_set.filter(
            judging_round=self.judging_round).first()
        if commitment:
            if commitment.capacity < goal:
                commitment.capacity = goal
            if commitment.current_quota < goal:
                commitment.current_quota = goal
            commitment.save()

    def _judge_assignment_count(self):
        scenarios = Scenario.objects.filter(
            judging_round=self.judging_round,
            is_active=True)
        return self.judge.judgepanelassignment_set.filter(
            scenario__in=scenarios,
            judge=self.judge).count()

    def _make_panel(self, choices):
        self._enable_additional_assignments(len(choices))
        panel = Panel(status=ACTIVE_PANEL_STATUS)
        panel.save()
        jpa = JudgePanelAssignment(
            judge=self.judge,
            panel=panel,
            scenario=self.scenario,
            assignment_status=ASSIGNED_PANEL_ASSIGNMENT_STATUS)
        jpa.save()
        for choice in choices:
            ApplicationPanelAssignment(
                application_id=choice,
                panel=panel,
                scenario=self.scenario).save()

    def _find_scenario(self):
        judging_round = self.judging_round
        if not hasattr(judging_round, "allocator"):
            scenario = Scenario(judging_round=judging_round,
                                is_active=True)
            scenario.save()
            Allocator(judging_round=judging_round,
                      scenario=scenario).save()
        return judging_round.allocator.scenario

    def _failure(self):
        return Response(status=403,
                        data=self.errors)
