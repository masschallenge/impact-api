# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.views.post_mixin import PostMixin
from impact.v1.helpers import CriterionHelper
from impact.v1.helpers.validators import INVALID_INTEGER_ERROR

class CriterionListView(BaseListView,
                        PostMixin):
    view_name = "criterion"
    helper_class = CriterionHelper
    actions = ['GET', 'POST']  # Should get this from PostMixin

    def get(self, request):
        self._validate_judging_round_id(request)
        return super().get(request)
    
    def _validate_judging_round_id(self, request):
        judging_round_id = request.query_params.get("judging_round_id")
        if judging_round_id is not None:
            try:
                judging_round_id = int(judging_round_id)
            except ValueError:
                self.errors.append(INVALID_INTEGER_ERROR % ("judging_round_id",
                                                            judging_round_id))
        
    def filter(self, qs):
        return self._filter_by_judging_round_id(qs)

    def _filter_by_judging_round_id(self, qs):
        judging_round_id = self.request.query_params.get("judging_round_id", None)
        if judging_round_id is not None:
            return qs.filter(judging_round_id=judging_round_id)
        return qs

    
