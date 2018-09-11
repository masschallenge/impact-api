# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import ApplicationHelper
from impact.v1.views.base_detail_view import BaseDetailView


class ApplicationDetailView(BaseDetailView):
    view_name = "application_detail"
    helper_class = ApplicationHelper
