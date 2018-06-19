# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    CriterionOptionSpec,
    JudgingRound,
)
from rest_framework.response import Response
from impact.v1.views.impact_view import ImpactView
from impact.v1.helpers.model_helper import (
    READ_ONLY_ID_FIELD,
    READ_ONLY_STRING_FIELD,
)


ANALYZE_JUDGING_ROUND_FIELDS = {
    "criterion_option_spec_id": READ_ONLY_ID_FIELD,
    "criterion_name": READ_ONLY_STRING_FIELD,
    "option": READ_ONLY_STRING_FIELD,
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
        results = [self.analyze_option(option) for option in options]
        return Response({"results": results})

    def analyze_option(self, option):
        return {
            "criterion_option_spec_id": option.id,
            "criterion_name": option.criterion.name,
            "option": option.option,
        }
