# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import JudgingRoundHelper


class JudgingRoundListView(BaseListView):
    view_name = "judging_round"
    helper_class = JudgingRoundHelper
