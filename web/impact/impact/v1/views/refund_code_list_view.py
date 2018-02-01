# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import RefundCodeHelper


class RefundCodeListView(BaseListView):
    view_name = "refund_code"
    helper_class = RefundCodeHelper
