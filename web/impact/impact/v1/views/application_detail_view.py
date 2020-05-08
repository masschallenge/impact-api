# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.helpers import ApplicationHelper
from .v1.views.base_detail_view import BaseDetailView


class ApplicationDetailView(BaseDetailView):
    view_name = "application_detail"
    helper_class = ApplicationHelper
