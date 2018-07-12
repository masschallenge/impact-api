# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from itertools import chain
from accelerator.models import (
    JudgingRound,
    User,
)
from rest_framework.response import Response
from impact.v1.views.impact_view import ImpactView


class AllocateApplicationsView(ImpactView):
    view_name = "allocate_applications"
    model = JudgingRound

    def get(self, request, round_id, judge_id):
        self.judging_round = JudgingRound.objects.get(pk=round_id)
        self.judge = User.objects.get(pk=judge_id)
        return Response(status=204)
