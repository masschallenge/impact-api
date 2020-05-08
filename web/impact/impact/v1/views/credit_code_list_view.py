# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_list_view import BaseListView
from ..helpers import CreditCodeHelper


class CreditCodeListView(BaseListView):
    view_name = "credit_code"
    helper_class = CreditCodeHelper
