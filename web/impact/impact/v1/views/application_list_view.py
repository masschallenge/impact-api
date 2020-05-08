# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import ApplicationHelper
from .base_list_view import BaseListView


class ApplicationListView(BaseListView):
    view_name = "application"
    helper_class = ApplicationHelper
