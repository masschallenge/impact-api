# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.helpers import ProgramCycleHelper
from .v1.views.base_detail_view import BaseDetailView


class ProgramCycleDetailView(BaseDetailView):
    view_name = "program_cycle_detail"
    helper_class = ProgramCycleHelper
