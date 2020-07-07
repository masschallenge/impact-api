# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from rest_framework.response import Response

from mc.models import JudgingRound
from mc.permission_checks import global_manager_check
from .impact_view import ImpactView
from ..helpers import (
    CriterionHelper,
    CriterionOptionSpecHelper,
)

ROUND_DOES_NOT_EXIST_ERROR = "Judging Round {} does not exist"
SOURCE_JUDGING_ROUND_KEY = 'source_judging_round_id'
TARGET_JUDGING_ROUND_KEY = 'target_judging_round_id'


class CloneCriteriaView(ImpactView):
    '''Endpoint for duplicating criteria state from an existing
    judging round onto a new round. Deletes any existing criteria
    and options on the target round.
    '''

    view_name = "clone_criteria"
    model = JudgingRound

    @classmethod
    def fields(cls):
        return {}

    def post(self, request):
        source_pk = request.data.get(SOURCE_JUDGING_ROUND_KEY)
        target_pk = request.data.get(TARGET_JUDGING_ROUND_KEY)
        self._validate_judging_round_exists(source_pk)
        self._validate_judging_round_exists(target_pk)
        if self.errors:
            return Response(status=401, data=self.errors)
        target_round = JudgingRound.objects.get(pk=target_pk)
        program_family = target_round.program.program_family
        global_manager_check(request.user, program_family)
        clones = CriterionHelper.clone_criteria(source_pk, target_pk)
        CriterionOptionSpecHelper.clone_option_specs(clones)
        return Response(status=204)

    def _validate_judging_round_exists(self, id):
        if not JudgingRound.objects.filter(pk=id).exists():
            self.errors.append(ROUND_DOES_NOT_EXIST_ERROR.format(id))
