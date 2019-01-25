# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import OrderedDict
from numpy import (
    array,
    matrix,
)

from django.db.models import Count
from itertools import chain
from accelerator.models import (
    Application,
    CriterionOptionSpec,
    JudgePanelAssignment,
    JudgingRound,

)
from rest_framework.response import Response
from impact.v1.views import ImpactView
from impact.v1.views.utils import find_criterion_helpers
from impact.v1.classes.option_analysis import OptionAnalysis
from impact.v1.helpers.model_helper import (
    READ_ONLY_ID_FIELD,
    READ_ONLY_INTEGER_FIELD,
    READ_ONLY_OBJECT_FIELD,
    READ_ONLY_STRING_FIELD,
)
from impact.permissions import global_operations_manager_check
from impact.v1.classes.application_data_cache import ApplicationDataCache
from impact.v1.classes.criteria_data_cache import CriteriaDataCache
from impact.v1.classes.judge_data_cache import JudgeDataCache
from impact.v1.classes.option_analysis import feedbacks_for_judging_round


ASSIGNMENT_DISCOUNT = 1
ANALYZE_JUDGING_ROUND_FIELDS = {
    "criterion_option_spec_id": READ_ONLY_ID_FIELD,
    "criterion_id": READ_ONLY_ID_FIELD,
    "weight": READ_ONLY_INTEGER_FIELD,
    "count": READ_ONLY_INTEGER_FIELD,
    "criterion_name": READ_ONLY_STRING_FIELD,
    "criterion_type": READ_ONLY_STRING_FIELD,
    "option": READ_ONLY_STRING_FIELD,
    "total_required_reads": READ_ONLY_INTEGER_FIELD,
    "completed_required_reads": READ_ONLY_INTEGER_FIELD,
    "needs_distribution": READ_ONLY_OBJECT_FIELD,
    "satisfied_apps": READ_ONLY_INTEGER_FIELD,
    "needy_apps": READ_ONLY_INTEGER_FIELD,
    "remaining_needed_reads": READ_ONLY_INTEGER_FIELD,
    "total_capacity": READ_ONLY_INTEGER_FIELD,
    "remaining_capacity": READ_ONLY_INTEGER_FIELD,
}


class AnalyzeJudgingRoundView(ImpactView):
    view_name = "analyze_judging_round"
    model = JudgingRound
    permission_classes = ()

    @classmethod
    def fields(cls):
        return ANALYZE_JUDGING_ROUND_FIELDS

    def get(self, request, pk):
        self._option_counts_cache = None
        self.instance = self.model.objects.get(pk=pk)
        self.apps = Application.objects.filter(
            application_status="submitted",
            application_type=self.instance.application_type)        
        self.judges = self.instance.confirmed_judge_label.users
        self.feedback = feedbacks_for_judging_round(
            self.instance, self.apps).order_by("application_id")        
        program_family = self.instance.program.program_family
        cleared = global_operations_manager_check(request.user, program_family)
        if not cleared:
            return Response(status=403)
        options = CriterionOptionSpec.objects.filter(
            criterion__judging_round=self.instance).prefetch_related(
                'criterion')
        application_counts = self.judge_to_count()
        app_ids = self.apps.values_list('id', flat=True)
        self.criterion_helpers = find_criterion_helpers(self.instance)
        self.criteria = tuple([helper.subject for helper in self.criterion_helpers.values()])
        needs = self._analyze()
        analyses = [OptionAnalysis(
            option,
            self.apps,
            app_ids,
            self.instance,
            application_counts,
            self.criterion_helpers
            needs).analyses()
            for option in options]
        return Response({"results": list(chain.from_iterable(analyses))})

    
    def _analyze(self):
        self._criteria_cache = CriteriaDataCache(
            self.apps,
            self.instance,
            self.criterion_helpers.values())
        self._application_cache = ApplicationDataCache(
            self.apps,
            self.criteria,
            self.feedback,
            self.criterion_helpers.values())        
        self.judge_data_cache = JudgeDataCache(
            self.judges,
            self.criteria,
            self.criterion_helpers.values())
        weights = self._criteria_cache.weights
        return self._application_needs()



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
                    (ASSIGNMENT_DISCOUNT *
                     self._sum_judge_data(key, app_data["assignments"])))
            else:
                needs[key] = 0
        return array(list(needs.values()))

    def _sum_judge_data(self, key, judge_ids):
        result = 0
        criterion, option = key
        for judge_id in judge_ids:
            judge_data = self.judge_data_cache.data.get(judge_id, {})
            helper = self.criterion_helpers.get(criterion.id)
            if helper.judge_matches_option(judge_data, option):
                result += 1
        return result
    
    def _option_counts(self, key):
        if self._option_counts_cache is None:
            self._option_counts_cache = {}
            for criterion in self.instance.criterion_set.all():
                self._add_criterion_options_to_cache(criterion)
        return self._option_counts_cache[key]

    def _add_criterion_options_to_cache(self, criterion):
        helper = self.criterion_helpers.get(criterion.id)
        for spec in criterion.criterionoptionspec_set.all():
            for option in helper.options(spec, self.apps):
                self._option_counts_cache[(criterion, option)] = spec.count
    
    def judge_to_count(self):
        assignments = JudgePanelAssignment.objects.filter(
            scenario__judging_round=self.instance)
        judge_assignment_counts = assignments.annotate(
            assignment_count=Count("panel__applications")).values_list(
                "judge_id", "assignment_count")
        results = {}
        for judge_id, assignment_count in judge_assignment_counts:
            results[judge_id] = results.get(judge_id, 0) + assignment_count
        return results
