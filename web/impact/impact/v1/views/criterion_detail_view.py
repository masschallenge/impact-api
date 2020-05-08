# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.views.patch_mixin import PatchMixin
from .v1.views.base_detail_view import BaseDetailView
from .v1.helpers import CriterionHelper


class CriterionDetailView(BaseDetailView,
                          PatchMixin):
    view_name = "criterion"
    helper_class = CriterionHelper
    actions = ["GET", "PATCH"]
