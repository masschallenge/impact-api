# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_list_view import BaseListView
from .post_mixin import PostMixin
from ..helpers import CriterionHelper


class CriterionListView(BaseListView,
                        PostMixin):
    view_name = "criterion"
    helper_class = CriterionHelper
    actions = ['GET', 'POST']  # Should get this from PostMixin

    def get(self, request):
        self.validate_id(request, 'judging_round_id')

        return super().get(request)

    def filter(self, qs):
        return self._filter_by_judging_round_id(super().filter(qs))

    def _filter_by_judging_round_id(self, qs):
        return self.filter_by_field("judging_round", qs)
