# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_list_view import BaseListView
from ..helpers import ProgramHelper


class ProgramListView(BaseListView):
    view_name = "program"
    helper_class = ProgramHelper
