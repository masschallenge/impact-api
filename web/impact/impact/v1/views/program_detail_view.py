# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import ProgramHelper
from impact.v1.views.base_detail_view import BaseDetailView


class ProgramDetailView(BaseDetailView):
    view_name = "program_detail"
    helper_class = ProgramHelper
