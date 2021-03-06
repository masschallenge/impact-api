# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_detail_view import BaseDetailView
from impact.v1.views.patch_mixin import PatchMixin
from impact.v1.helpers import CriterionOptionSpecHelper


class CriterionOptionSpecDetailView(BaseDetailView, PatchMixin):
    actions = ["GET", "PATCH"]
    view_name = "criterion_option_spec"
    helper_class = CriterionOptionSpecHelper
