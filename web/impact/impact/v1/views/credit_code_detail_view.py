# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import CreditCodeHelper
from impact.v1.views.base_detail_view import BaseDetailView


class CreditCodeDetailView(BaseDetailView):
    view_name = "credit_code_detail"
    helper_class = CreditCodeHelper
