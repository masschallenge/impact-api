# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeGenderCriterionHelper(CriterionHelper):
    def query_for_option(self, query, option_name):
        return query.filter(judge__expertprofile__gender=option_name[0])
