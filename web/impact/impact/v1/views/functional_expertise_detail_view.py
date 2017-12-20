# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import FunctionalExpertiseHelper
from impact.v1.views.base_detail_view import BaseDetailView


class FunctionalExpertiseDetailView(BaseDetailView):
    view_name = "functional_expertise_detail"
    helper_class = FunctionalExpertiseHelper
