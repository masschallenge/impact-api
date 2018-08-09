# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from itertools import chain
from accelerator.models import (
    Application,
    CriterionOptionSpec,
    JudgingRound,
)
from rest_framework.response import Response
from impact.v1.views.impact_view import ImpactView
from impact.v1.classes.option_analysis import OptionAnalysis
from impact.v1.helpers.model_helper import (
    READ_ONLY_ID_FIELD,
    READ_ONLY_INTEGER_FIELD,
    READ_ONLY_OBJECT_FIELD,
    READ_ONLY_STRING_FIELD,
)


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

    @classmethod
    def fields(cls):
        return ANALYZE_JUDGING_ROUND_FIELDS

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        options = CriterionOptionSpec.objects.filter(
            criterion__judging_round=self.instance)
        self.apps = Application.objects.filter(
            application_status="submitted",
            application_type=self.instance.application_type)
        analyses = [OptionAnalysis(option, self.apps, self.instance).analyses()
                    for option in options]
        return Response({"results": list(chain.from_iterable(analyses))})
