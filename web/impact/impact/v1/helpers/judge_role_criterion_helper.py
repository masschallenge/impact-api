# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.judge_criterion_helper import JudgeCriterionHelper


class JudgeRoleCriterionHelper(JudgeCriterionHelper):
    def filter_by_judge_option(self, query, option_name):
        return query.filter(
            judge__expertprofile__expert_category__name=option_name)

    def judge_field(self):
        return "expertprofile__expert_category__name"
