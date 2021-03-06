# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import (
    defaultdict,
    OrderedDict,
)
from numpy import (
    array,
    matmul,
)
from impact.v1.classes.application_data_cache import ApplicationDataCache
from impact.v1.classes.criteria_data_cache import CriteriaDataCache
from impact.v1.classes.judge_data_cache import JudgeDataCache
from accelerator.models import (
    ACTIVE_PANEL_STATUS,
    Allocator,
    Application,
    ApplicationPanelAssignment,
    ASSIGNED_PANEL_ASSIGNMENT_STATUS,
    JudgePanelAssignment,
    JudgingRound,
    Panel,
    Scenario,
    User,
)
from rest_framework.response import Response
from impact.v1.helpers import CriterionHelper
from impact.v1.views.impact_view import ImpactView
from impact.permissions import (
    AllocateApplicationsPermissions,
)
from impact.v1.classes.option_analysis import feedbacks_for_judging_round

ALREADY_ASSIGNED_ERROR = "{judge} is already assigned to {count} applications"
JUDGING_ROUND_INACTIVE_ERROR = "Judging round {} is not active"
NO_APP_LEFT_FOR_JUDGE = "{} has provided feedback on all applications"
NO_DATA_FOR_JUDGE = "Judging round {judging_round} has no data for {judge}"
ASSIGNMENT_DISCOUNT = 0.45
ASSIGNMENT_STALE_DAYS = 7.0
ASSIGNMENT_STALE_SECONDS = ASSIGNMENT_STALE_DAYS * 24 * 60 * 60


class AllocateApplicationsView(ImpactView):
    '''Endpoint for allocation of applications to a judge.'''
    permission_classes = (
        AllocateApplicationsPermissions,
    )
    view_name = "allocate_applications"

    def __init__(self):
        self._app_id_cache = None
        self._option_counts_cache = None
        self.errors = []

    def get(self, request, round_id, judge_id):
        self._initialize(round_id, judge_id)
        if self.errors:
            return self._failure()
        applications = self._allocate()
        if self.errors:
            return self._failure()
        return Response(applications)

    def _initialize(self, round_id, judge_id):
        self.judging_round = JudgingRound.objects.get(pk=round_id)
        self.judge = User.objects.get(pk=judge_id)
        self.scenario = self._find_scenario()
        self._check_judging_round()
        self._check_assignments()
        if self.errors:
            return
        self.apps = Application.objects.filter(
            application_type=self.judging_round.application_type,
            application_status="submitted").order_by("id")
        self.judges = self.judging_round.confirmed_judge_label.users
        self.feedback = feedbacks_for_judging_round(
            self.judging_round, self.apps).order_by("application_id")
        self.criteria = self.judging_round.criterion_set.all()
        self.criterion_helpers = find_criterion_helpers(self.judging_round)
        self._criteria_cache = CriteriaDataCache(
            self.apps,
            self.judging_round,
            self.criterion_helpers.values())
        self._application_cache = ApplicationDataCache(
            self.apps,
            self.criteria,
            self.feedback,
            self.criterion_helpers.values())
        self._judge_cache = JudgeDataCache(
            self.judges,
            self.criteria,
            self.criterion_helpers.values())
        if not self._judge_cache.data.get(self.judge.id, {}):
            self.errors.append(NO_DATA_FOR_JUDGE.format(
                judging_round=self.judging_round,
                judge=self.judge.email))

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
        weights = self._criteria_cache.weights
        judge_features = self._judge_cache.features(self.judge, weights)
        needs = self._application_needs()
        needs_matrix = array(needs * array(list(weights.values())))
        preferences = matmul(judge_features, needs_matrix.transpose())
        choices = self._choose_app_ids(preferences)
        if not choices:
            self.errors.append(NO_APP_LEFT_FOR_JUDGE.format(self.judge.email))
        else:
            self._make_panel(choices)
        return choices

    def _application_needs(self):
        rows = []
        for app_id in self.apps.values_list("id", flat=True):
            rows.append(self._application_need(app_id))
        return array(rows)

    def _application_need(self, app_id):
        needs = OrderedDict()
        app_data = self._application_cache.data[app_id]
        fields = app_data["fields"]
        keys = self._criteria_cache.weights.keys()
        for key in keys:
            criterion, option = key
            helper = self.criterion_helpers.get(criterion.id)
            if helper.field_matches_option(fields[helper.application_field],
                                           option):
                needs[key] = (
                    self._option_counts(key) -
                    self._sum_judge_data(key, app_data["feedbacks"]) -
                    self._sum_judge_data(
                        key,
                        app_data["assignments"],
                        assignment_ages=app_data['assignment_ages']))
            else:
                needs[key] = 0
        return array(list(needs.values()))

    def _option_counts(self, key):
        if self._option_counts_cache is None:
            self._option_counts_cache = {}
            for criterion in self.judging_round.criterion_set.all():
                self._add_criterion_options_to_cache(criterion)
        return self._option_counts_cache[key]

    def _add_criterion_options_to_cache(self, criterion):
        helper = self.criterion_helpers.get(criterion.id)
        for spec in criterion.criterionoptionspec_set.all():
            for option in helper.options(spec, self.apps):
                self._option_counts_cache[(criterion, option)] = spec.count

    def _sum_judge_data(self, key, judge_ids, assignment_ages=None):
        assignment_ages = assignment_ages or defaultdict(int)
        result = 0
        criterion, option = key
        for judge_id in judge_ids:
            judge_data = self._judge_cache.data.get(judge_id, {})
            helper = self.criterion_helpers.get(criterion.id)
            if helper.judge_matches_option(judge_data, option):
                result += calc_discount(judge_id, assignment_ages)
        return result

    def _choose_app_ids(self, preferences):
        panel_size = self.scenario.panel_size
        apps = (array(self.apps)[(-preferences).argsort()]).flat
        result = []
        count = 0
        for app in apps:
            if app.id not in self.app_ids():
                result.append(app.id)
                count += 1
            if count >= panel_size:
                break
        return result

    def app_ids(self):
        if self._app_id_cache is None:
            self._app_id_cache = self._assignments().values_list(
                "panel__applicationpanelassignment__application_id",
                flat=True)
        return self._app_id_cache

    def _assignments(self):
        return self.judge.judgepanelassignment_set.filter(
            scenario__judging_round=self.judging_round)

    def _incomplete_assignments(self):
        return self._assignments().filter(
            assignment_status=ASSIGNED_PANEL_ASSIGNMENT_STATUS)

    def _make_panel(self, choices):
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


def find_criterion_helpers(judging_round):
    c_set = judging_round.criterion_set.all()
    return {criterion.id: CriterionHelper.find_helper(criterion)
            for criterion in c_set}


def calc_discount(judge_id, assignment_ages):
    age = assignment_ages[judge_id]
    age_score = (ASSIGNMENT_STALE_SECONDS - age) / ASSIGNMENT_STALE_SECONDS
    return max(0, age_score)
