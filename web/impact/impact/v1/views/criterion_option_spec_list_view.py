# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.post_mixin import PostMixin
from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import CriterionOptionSpecHelper


class CriterionOptionSpecListView(BaseListView,
                                  PostMixin):
    helper_class = CriterionOptionSpecHelper
    view_name = "criterion_option_spec"
    actions = ['GET', 'POST']  # Should get this from PostMixin

    def get(self, request):
        self.validate_id(request, 'judging_round_id')
        self.validate_id(request, 'criterion_id')
        return super().get(request)

    def filter(self, qs):
        qs = self._filter_by_criterion_id(qs)
        return self._filter_by_judging_round_id(qs)

    def _filter_by_judging_round_id(self, qs):
        lookup = "criterion__judging_round_id"
        return self.filter_by_field("judging_round_id", qs, lookup)

    def _filter_by_criterion_id(self, qs):
        return self.filter_by_field("criterion_id", qs)
