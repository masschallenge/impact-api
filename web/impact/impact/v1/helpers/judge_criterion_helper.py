# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeCriterionHelper(CriterionHelper):
    def filter_by_judge_option(self, query, option_name):
        key = "judge__" + self.judge_field
        return query.filter(**{key: option_name})

    def option_for_field(self, field):
        return field
