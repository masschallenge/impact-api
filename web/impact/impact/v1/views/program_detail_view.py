# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import ProgramHelper
from .base_detail_view import BaseDetailView


class ProgramDetailView(BaseDetailView):
    view_name = "program_detail"
    helper_class = ProgramHelper
