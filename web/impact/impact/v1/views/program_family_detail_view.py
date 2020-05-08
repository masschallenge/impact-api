# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import ProgramFamilyHelper
from .base_detail_view import BaseDetailView


class ProgramFamilyDetailView(BaseDetailView):
    view_name = "program_family_detail"
    helper_class = ProgramFamilyHelper
