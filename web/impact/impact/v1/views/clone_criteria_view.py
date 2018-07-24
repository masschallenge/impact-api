# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from rest_framework.response import Response

from accelerator.models import JudgingRound
from impact.v1.views.impact_view import ImpactView
from impact.v1.helpers.model_helper import (
    READ_ONLY_ID_FIELD,
    READ_ONLY_INTEGER_FIELD,
    READ_ONLY_OBJECT_FIELD,
    READ_ONLY_STRING_FIELD,
)
from impact.v1.helpers import (
    CriterionHelper,
    CriterionOptionSpecHelper,
)

ANALYZE_JUDGING_ROUND_FIELDS = {
    "criterion_option_spec_id": READ_ONLY_ID_FIELD,
    "weight": READ_ONLY_INTEGER_FIELD,
    "count": READ_ONLY_INTEGER_FIELD,
    "criterion_name": READ_ONLY_STRING_FIELD,
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


class CloneCriteriaView(ImpactView):
    view_name = "clone_criteria"
    model = JudgingRound

    @classmethod
    def fields(cls):
        return ANALYZE_JUDGING_ROUND_FIELDS

    def get(self, request, source_pk, target_pk):
        clones = CriterionHelper.clone_criteria(source_pk, target_pk)
        CriterionOptionSpecHelper.clone_option_specs(clones)
        return Response({"results": "Success"})
