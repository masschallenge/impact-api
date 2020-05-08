# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.views.base_list_view import BaseListView
from .v1.helpers import ProgramHelper


class ProgramListView(BaseListView):
    view_name = "program"
    helper_class = ProgramHelper
