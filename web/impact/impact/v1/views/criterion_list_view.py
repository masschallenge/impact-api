# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.views.post_mixin import PostMixin
from impact.v1.helpers import CriterionHelper


class CriterionListView(BaseListView,
                        PostMixin):
    view_name = "criterion"
    helper_class = CriterionHelper
    actions = ['GET', 'POST']  # Should get this from PostMixin

    def get(self, request):
        self.validate_id(request, 'judging_round_id')
        return super().get(request)

    def filter(self, qs):
        return self._filter_by_judging_round_id(qs)

    def _filter_by_judging_round_id(self, qs):
        judging_round_id = self.request.query_params.get("judging_round_id",
                                                         None)
        if judging_round_id is not None:
            return qs.filter(judging_round_id=judging_round_id)
        return qs
