# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_list_view import BaseListView
from ..helpers import IndustryHelper


class IndustryListView(BaseListView):
    view_name = "industry"
    helper_class = IndustryHelper
