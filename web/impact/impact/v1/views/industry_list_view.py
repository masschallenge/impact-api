# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import IndustryHelper


class IndustryListView(BaseListView):
    view_name = "industry"
    helper_class = IndustryHelper
