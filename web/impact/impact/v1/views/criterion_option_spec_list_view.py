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
        self._validate_judging_round_id(request)
        self._validate_criterion_id(request)
        return super().get(request)
    
    def _validate_judging_round_id(self, request):
        judging_round_id = request.query_params.get("judging_round_id")
        if judging_round_id is not None:
            try:
                judging_round_id = int(judging_round_id)
            except ValueError:
                self.errors.append(INVALID_INTEGER_ERROR % ("judging_round_id",
                                                            judging_round_id))

    def _validate_criterion_id(self, request):
        criterion_id = request.query_params.get("criterion_id")
        if criterion_id is not None:
            try:
                criterion_id = int(criterion_id)
            except ValueError:
                self.errors.append(INVALID_INTEGER_ERROR % ("criterion_id",
                                                            criterion_id))
                
    def filter(self, qs):
        qs = self._filter_by_criterion_id(qs)
        return self._filter_by_judging_round_id(qs)

    def _filter_by_judging_round_id(self, qs):
        judging_round_id = self.request.query_params.get("judging_round_id", None)
        if judging_round_id is not None:
            return qs.filter(criterion__judging_round_id=judging_round_id)
        return qs

    def _filter_by_criterion_id(self, qs):
        criterion_id = self.request.query_params.get("criterion_id", None)
        if criterion_id is not None:
            return qs.filter(criterion_id=criterion_id)
        return qs
    
