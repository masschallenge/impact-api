# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.list_view import ListView
from impact.v1.helpers import ProgramFamilyHelper
from impact.v1.views.program_family_detail_view import ProgramFamilyDetailView


class ProgramFamilyListView(ListView):
    helper_class = ProgramFamilyHelper
    METADATA_ACTIONS = ProgramFamilyDetailView.METADATA_ACTIONS
