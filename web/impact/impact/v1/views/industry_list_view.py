# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.views.base_list_view import BaseListView
from .v1.helpers import IndustryHelper


class IndustryListView(BaseListView):
    view_name = "industry"
    helper_class = IndustryHelper
