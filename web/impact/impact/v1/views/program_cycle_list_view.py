# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import ProgramCycleHelper


class ProgramCycleListView(BaseListView):
    view_name = "program_cycle"
    helper_class = ProgramCycleHelper
