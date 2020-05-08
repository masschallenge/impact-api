# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import FunctionalExpertiseHelper
from .base_detail_view import BaseDetailView


class FunctionalExpertiseDetailView(BaseDetailView):
    view_name = "functional_expertise_detail"
    helper_class = FunctionalExpertiseHelper
