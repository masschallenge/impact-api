# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .v1.views.base_detail_view import BaseDetailView
from .v1.views.patch_mixin import PatchMixin
from .v1.helpers import CriterionOptionSpecHelper


class CriterionOptionSpecDetailView(BaseDetailView, PatchMixin):
    actions = ["GET", "PATCH"]
    view_name = "criterion_option_spec"
    helper_class = CriterionOptionSpecHelper
