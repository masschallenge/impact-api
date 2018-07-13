# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeRoleCriterionHelper(CriterionHelper):
    def query_for_option(self, query, option_name):
        return query.filter(
            judge__expertprofile__expert_category__name=option_name)
