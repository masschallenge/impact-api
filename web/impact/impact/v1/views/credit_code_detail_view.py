# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import CreditCodeHelper
from .base_detail_view import BaseDetailView


class CreditCodeDetailView(BaseDetailView):
    view_name = "credit_code_detail"
    helper_class = CreditCodeHelper
