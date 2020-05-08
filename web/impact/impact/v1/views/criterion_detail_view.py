# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .patch_mixin import PatchMixin
from .base_detail_view import BaseDetailView
from ..helpers import CriterionHelper


class CriterionDetailView(BaseDetailView,
                          PatchMixin):
    view_name = "criterion"
    helper_class = CriterionHelper
    actions = ["GET", "PATCH"]
