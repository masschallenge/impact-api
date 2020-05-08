# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_list_view import BaseListView
from ..helpers import ProgramCycleHelper


class ProgramCycleListView(BaseListView):
    view_name = "program_cycle"
    helper_class = ProgramCycleHelper
