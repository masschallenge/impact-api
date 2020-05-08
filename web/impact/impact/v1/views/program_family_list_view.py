# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_list_view import BaseListView
from ..helpers import ProgramFamilyHelper


class ProgramFamilyListView(BaseListView):
    view_name = "program_family"
    helper_class = ProgramFamilyHelper
