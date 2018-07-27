from collections import OrderedDict
from impact.v1.helpers import CriterionHelper


class CriteriaDataCache(object):
    def __init__(self):
        self._criteria = None
        self._weights = None

    def criteria(self, judging_round):
        if self._criteria is None:
            self._criteria = judging_round.criterion_set.all()
        return self._criteria
        
    def weights(self, judging_round, apps):
        if self._weights is None:
            self._weights = OrderedDict()
            for criterion in self.criteria(judging_round):
                helper = CriterionHelper.find_helper(criterion)
                self._add_specs(helper, apps)
        return self._weights

    def _add_specs(self, helper, apps):
        criterion = helper.subject
        for spec in criterion.criterionoptionspec_set.all():
            for option in helper.options(spec, apps):
                key = (criterion, option)
                self._weights[key] = float(spec.weight)
