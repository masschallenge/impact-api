# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_detail_view import BaseDetailView
from .patch_mixin import PatchMixin
from ..helpers import CriterionOptionSpecHelper


class CriterionOptionSpecDetailView(BaseDetailView, PatchMixin):
    actions = ["GET", "PATCH"]
    view_name = "criterion_option_spec"
    helper_class = CriterionOptionSpecHelper
