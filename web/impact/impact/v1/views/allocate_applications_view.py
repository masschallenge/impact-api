# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import OrderedDict
from numpy import (
    array,
    matrix,
)
from accelerator.models import (
    ACTIVE_PANEL_STATUS,
    Allocator,
    Application,
    ApplicationPanelAssignment,
    ASSIGNED_PANEL_ASSIGNMENT_STATUS,
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JUDGING_FEEDBACK_STATUS_INCOMPLETE,
    JudgePanelAssignment,
    JudgingRound,
    Panel,
    Scenario,
    User,
)
from rest_framework.response import Response
from impact.v1.helpers import CriterionHelper
from impact.v1.views.impact_view import ImpactView
from impact.v1.classes.allocate_applications_permissions import (
    AllocateApplicationsPermissions,
)
from impact.v1.classes.option_analysis import feedbacks_for_judging_round

ALREADY_ASSIGNED_ERROR = "{judge} is already assigned to {count} applications"
JUDGING_ROUND_INACTIVE_ERROR = "Judging round {} is not active"
NO_APP_LEFT_FOR_JUDGE = "{} has provided feedback on all applications"
NO_DATA_FOR_JUDGE = "Judging round {judging_round} has no data for {judge}"
ASSIGNMENT_DISCOUNT = 0.85


class AllocateApplicationsView(ImpactView):
    permission_classes = (
        AllocateApplicationsPermissions,
    )
    view_name = "allocate_applications"

    def __init__(self):
        self._app_assignments_cache = None
        self._app_data_cache = None
        self._app_reads_cache = None
        self._criteria_cache = None
        self._criteria_weights_cache = None
        self._judge_app_id_cache = None
        self._judge_data_cache = None
        self._option_counts_cache = None
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
        count = self._incomplete_assignments().count()
        if count > 0:
            self.errors.append(ALREADY_ASSIGNED_ERROR.format(
                judge=self.judge.email, count=count))

    def _allocate(self):
        self.apps = Application.objects.filter(
            application_type=self.judging_round.application_type,
            application_status="submitted").order_by("id")
        self.feedback = feedbacks_for_judging_round(
            self.judging_round, self.apps).order_by("application_id")
        self.judges = self.judging_round.confirmed_judge_label.users
        judge_features = self._judge_features()
        if self.errors:
            return []
        needs = self._application_needs()
        weights = array(list(self._criteria_weights().values()))
        needs_matrix = matrix(needs * weights)
        preferences = judge_features * needs_matrix.transpose()
        choices = self._choose_app_ids(preferences)
        if not choices:
            self.errors.append(NO_APP_LEFT_FOR_JUDGE.format(self.judge.email))
        else:
            self._make_panel(choices)
        return choices

    def _judge_features(self):
        datum = self._data_for_judge(self.judge)
        if not datum:
            return matrix([])
        keys = self._criteria_weights().keys()
        row = OrderedDict([(key, 0) for key in keys])
        for criterion in self._criteria():
            helper = CriterionHelper.find_helper(criterion)
            option = helper.option_for_field(
                datum[helper.judge_field])
            key = (criterion, option)
            if key in keys:
                row[key] = 1
        return matrix(list(row.values()))

    def _data_for_judge(self, judge):
        result = self._judge_data().get(judge.id, None)
        if not result:
            self.errors.append(NO_DATA_FOR_JUDGE.format(
                judging_round=self.judging_round,
                judge=self.judge.email))
        return result

    def _judge_data(self):
        if self._judge_data_cache is None:
            fields = set(["id"])
            result = {}
            for criterion in self._criteria():
                helper = CriterionHelper.find_helper(criterion)
                fields.add(helper.judge_field)
            for datum in self.judges.values(*list(fields)):
                result[datum["id"]] = datum
            self._judge_data_cache = result
        return self._judge_data_cache

    def _criteria_weights(self):
        if self._criteria_weights_cache is None:
            self._criteria_weights_cache = OrderedDict()
            for criterion in self._criteria():
                helper = CriterionHelper.find_helper(criterion)
                self._add_specs(helper)
        return self._criteria_weights_cache

    def _criteria(self):
        if self._criteria_cache is None:
            self._criteria_cache = self.judging_round.criterion_set.all()
        return self._criteria_cache

    def _add_specs(self, helper):
        criterion = helper.subject
        for spec in criterion.criterionoptionspec_set.all():
            for option in helper.options(spec, self.apps):
                key = (criterion, option)
                self._criteria_weights_cache[key] = float(spec.weight)

    def _application_data(self):
        if self._app_data_cache is None:
            fields = set(["id"])
            result = {}
            for criterion in self._criteria():
                helper = CriterionHelper.find_helper(criterion)
                fields.add(helper.application_field)
            for field_data in self.apps.values(*list(fields)):
                app_id = field_data["id"]
                result[app_id] = {
                    "fields": field_data,
                    "feedbacks": self._app_reads().get(app_id, []),
                    "assignments": self._app_assignments().get(app_id, [])
                }
            self._app_data_cache = result
        return self._app_data_cache

    def _app_reads(self):
        if self._app_reads_cache is None:
            app_to_judge = self.feedback.filter(
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE).values_list(
                "application_id", "judge_id")
            self._app_reads_cache = _collect_pairs(app_to_judge)
        return self._app_reads_cache

    def _app_assignments(self):
        if self._app_assignments_cache is None:
            assignments = ApplicationPanelAssignment.objects.filter(
                application__in=self.apps).values_list(
                    "application_id",
                    "panel__judgepanelassignment__judge_id")
            finished_assignments = self.feedback.exclude(
                feedback_status=JUDGING_FEEDBACK_STATUS_INCOMPLETE
            ).values_list("application_id", "judge_id")
            self._app_assignments_cache = _collect_pairs(
                set(assignments) - set(finished_assignments))
        return self._app_assignments_cache

    def _application_needs(self):
        rows = []
        for app_id in self.apps.values_list("id", flat=True):
            rows.append(self._application_need(app_id))
        return array(rows)

    def _application_need(self, app_id):
        needs = OrderedDict()
        app_data = self._application_data()[app_id]
        fields = app_data["fields"]
        keys = self._criteria_weights().keys()
        for key in keys:
            criterion, option = key
            helper = CriterionHelper.find_helper(criterion)
            if helper.field_matches_option(fields[helper.application_field],
                                           option):
                needs[key] = (
                    self._option_counts(key) -
                    self._sum_judge_data(key, app_data["feedbacks"]) -
                    self._assignment_weight(key, app_data["assignments"]))
            else:
                needs[key] = 0
        return array(list(needs.values()))

    def _assignment_weight(self, key, data):
        return ASSIGNMENT_DISCOUNT * self._sum_judge_data(key, data)

    def _option_counts(self, key):
        if self._option_counts_cache is None:
            cache = {}
            for criterion in self.judging_round.criterion_set.all():
                helper = CriterionHelper.find_helper(criterion)
                for spec in criterion.criterionoptionspec_set.all():
                    for option in helper.options(spec, self.apps):
                        cache[(criterion, option)] = spec.count
            self._option_counts_cache = cache
        return self._option_counts_cache[key]

    def _sum_judge_data(self, key, judge_ids):
        result = 0
        criterion, option = key
        for judge_id in judge_ids:
            judge_data = self._judge_data().get(judge_id, {})
            field = CriterionHelper.find_helper(criterion).judge_field
            if option == judge_data.get(field):
                result += 1
        return result

    def _choose_app_ids(self, preferences):
        panel_size = self.scenario.panel_size
        apps = (array(self.apps)[(-preferences).argsort()]).flat
        result = []
        count = 0
        for app in apps:
            if self._can_assign(app.id):
                result.append(app.id)
                count += 1
            if count >= panel_size:
                break
        return result

    def _can_assign(self, app_id):
        return app_id not in self._judge_app_ids()

    def _assignments(self):
        return self.judge.judgepanelassignment_set.filter(
            scenario__judging_round=self.judging_round)

    def _incomplete_assignments(self):
        return self._assignments().filter(
            assignment_status=ASSIGNED_PANEL_ASSIGNMENT_STATUS)

    def _judge_app_ids(self):
        if self._judge_app_id_cache is None:
            self._judge_app_id_cache = self._assignments().values_list(
                "panel__applicationpanelassignment__application_id",
                flat=True)
        return self._judge_app_id_cache

    def _make_panel(self, choices):
        self._enable_additional_assignments(len(choices))
        panel = Panel.objects.create(status=ACTIVE_PANEL_STATUS)
        JudgePanelAssignment.objects.create(
            judge=self.judge,
            panel=panel,
            scenario=self.scenario,
            assignment_status=ASSIGNED_PANEL_ASSIGNMENT_STATUS)
        for choice in choices:
            ApplicationPanelAssignment.objects.create(
                application_id=choice,
                panel=panel,
                scenario=self.scenario)

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

    def _find_scenario(self):
        judging_round = self.judging_round
        if not hasattr(judging_round, "allocator"):
            scenario = Scenario.objects.create(
                judging_round=judging_round, is_active=True)
            Allocator.objects.create(judging_round=judging_round,
                                     scenario=scenario)
        return judging_round.allocator.scenario

    def _failure(self):
        return Response(status=403,
                        data=self.errors)


def _collect_pairs(pairs):
    result = {}
    for first, second in pairs:
        value = result.get(first)
        if value:
            value.append(second)
        else:
            result[first] = [second]
    return result
