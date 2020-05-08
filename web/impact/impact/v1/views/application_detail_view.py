# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import ApplicationHelper
from .base_detail_view import BaseDetailView


class ApplicationDetailView(BaseDetailView):
    view_name = "application_detail"
    helper_class = ApplicationHelper
