from collections import OrderedDict
from numpy import array


class JudgeDataCache(object):
    def __init__(self, judges, criteria, criterion_helpers):
        self.criteria = criteria
        self.data = {}
        fields = set(["id"])
        self.criterion_helpers = criterion_helpers
        for helper in self.criterion_helpers:
            fields.add(helper.cache_judge_field)
        for datum in judges.values(*list(fields)):
            self.data[datum["id"]] = datum

    def features(self, judge, weights):
        datum = self.data.get(judge.id, {})
        if not datum:
            return array([])
        keys = weights.keys()
        row = OrderedDict([(key, 0) for key in keys])
        for helper in self.criterion_helpers:
            option = helper.option_for_field(
                datum[helper.cache_judge_field])
            key = (helper.subject, option)
            if key in keys:
                row[key] = 1
        return array(list(row.values()))
