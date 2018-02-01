# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import RefundCodeHelper
from impact.v1.views.base_detail_view import BaseDetailView


class RefundCodeDetailView(BaseDetailView):
    view_name = "refund_code_detail"
    helper_class = RefundCodeHelper
