# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.list_view import ListView
from impact.v1.helpers import IndustryHelper
from impact.v1.views.industry_detail_view import IndustryDetailView


class IndustryListView(ListView):
    helper_class = IndustryHelper
    METADATA_ACTIONS = IndustryDetailView.METADATA_ACTIONS
