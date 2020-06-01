# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from itertools import chain

from django.db.models import Count
from rest_framework.response import Response

from accelerator.models import CriterionOptionSpec
from mc.models import (
    Application,
    JudgePanelAssignment,
    JudgingRound,
)
from . import (
    find_criterion_helpers,
    ImpactView,
)
from ..classes.option_analysis import OptionAnalysis
from ..helpers.model_helper import (
    READ_ONLY_ID_FIELD,
    READ_ONLY_INTEGER_FIELD,
    READ_ONLY_OBJECT_FIELD,
    READ_ONLY_STRING_FIELD,
)
from ...permissions import global_operations_manager_check

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
    '''Endpoint for judging round analysis. Analysis logic is delegated to
    OptionAnalysis (and thence to CriterionHelpers)
    '''

    view_name = "analyze_judging_round"
    model = JudgingRound
    permission_classes = ()

    @classmethod
    def fields(cls):
        return ANALYZE_JUDGING_ROUND_FIELDS

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        program_family = self.instance.program.program_family
        if not global_operations_manager_check(request.user, program_family):
            return Response(status=403)
        options = CriterionOptionSpec.objects.filter(
            criterion__judging_round=self.instance).prefetch_related(
                'criterion')
        self.apps = Application.objects.filter(
            application_status="submitted",
            application_type=self.instance.application_type)
        application_counts = self.judge_to_count()
        app_ids = self.apps.values_list('id', flat=True)
        criterion_helpers = find_criterion_helpers(self.instance)
        option_analysis_instance = OptionAnalysis(
            self.apps,
            app_ids,
            self.instance,
            application_counts,
            criterion_helpers)
        analyses = [option_analysis_instance.analyses(option)
                    for option in options]
        return Response({"results": list(chain.from_iterable(analyses))})

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
