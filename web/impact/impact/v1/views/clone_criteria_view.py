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

ROUND_DOES_NOT_EXIST_ERROR = "Judging Round {} does not exist"


class CloneCriteriaView(ImpactView):
    view_name = "clone_criteria"
    model = JudgingRound

    @classmethod
    def fields(cls):
        return {}

    def post(self, request, source_pk, target_pk):
        self._validate_judging_round_exists(source_pk)
        self._validate_judging_round_exists(target_pk)
        if self.errors:
            return Response(status=401, data=self.errors)
        clones = CriterionHelper.clone_criteria(source_pk, target_pk)
        CriterionOptionSpecHelper.clone_option_specs(clones)
        return Response(status=204)

    def _validate_judging_round_exists(self, id):
        if not JudgingRound.objects.filter(pk=id).exists():
            self.errors.append(ROUND_DOES_NOT_EXIST_ERROR.format(id))
