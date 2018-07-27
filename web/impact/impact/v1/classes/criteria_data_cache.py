from collections import OrderedDict
from impact.v1.helpers import CriterionHelper


class CriteriaDataCache(object):
    def __init__(self, apps, judging_round):
        self.apps = apps
        self.judging_round = judging_round
        self.criteria = judging_round.criterion_set.all()
        self._calc_weights()

    def _calc_weights(self):
        self.weights = OrderedDict()
        for criterion in self.criteria:
            helper = CriterionHelper.find_helper(criterion)
            self._add_specs(helper)

    def _add_specs(self, helper):
        criterion = helper.subject
        for spec in criterion.criterionoptionspec_set.all():
            for option in helper.options(spec, self.apps):
                key = (criterion, option)
                self.weights[key] = float(spec.weight)
