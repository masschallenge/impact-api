# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import ApplicationHelper


class ApplicationListView(BaseListView):
    view_name = "application"
    helper_class = ApplicationHelper
