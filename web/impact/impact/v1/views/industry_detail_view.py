# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import IndustryHelper
from .base_detail_view import BaseDetailView


class IndustryDetailView(BaseDetailView):
    view_name = "industry_detail"
    helper_class = IndustryHelper
