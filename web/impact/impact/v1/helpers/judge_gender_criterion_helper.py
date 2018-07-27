# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.judge_criterion_helper import JudgeCriterionHelper


class JudgeGenderCriterionHelper(JudgeCriterionHelper):
    judge_field = "expertprofile__gender"
