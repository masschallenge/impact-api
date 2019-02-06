# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeCriterionHelper(CriterionHelper):
    def filter_by_judge_option(self, query, option_name):
        key = self.judge_field
        return query.filter(**{key: option_name})

    def option_for_field(self, field):
        return field

    def judge_matches_option(self, judge_data, option):
        return option == judge_data.get(self.cache_judge_field)

    def analysis_fields(self):
        return [
            self.judge_field,
        ]
