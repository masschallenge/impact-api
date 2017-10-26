# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import ProgramFamilyHelper
from impact.v1.views.base_detail_view import BaseDetailView


class ProgramFamilyDetailView(BaseDetailView):
    helper_class = ProgramFamilyHelper
