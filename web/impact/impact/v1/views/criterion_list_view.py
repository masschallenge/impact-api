# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import CriterionHelper


class CriterionListView(BaseListView):
    view_name = "criterion"
    helper_class = CriterionHelper
