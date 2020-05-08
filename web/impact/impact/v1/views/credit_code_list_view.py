# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.views.base_list_view import BaseListView
from .v1.helpers import CreditCodeHelper


class CreditCodeListView(BaseListView):
    view_name = "credit_code"
    helper_class = CreditCodeHelper
