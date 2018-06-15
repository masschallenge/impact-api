# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_detail_view import BaseDetailView
from impact.v1.helpers import CriterionHelper


class CriterionDetailView(BaseDetailView):
    view_name = "criterion"
    helper_class = CriterionHelper
