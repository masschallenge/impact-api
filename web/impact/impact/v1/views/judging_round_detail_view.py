# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import JudgingRoundHelper
from .base_detail_view import BaseDetailView


class JudgingRoundDetailView(BaseDetailView):
    view_name = "judging_round_detail"
    helper_class = JudgingRoundHelper
