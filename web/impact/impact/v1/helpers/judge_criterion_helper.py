# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeCriterionHelper(CriterionHelper):
    def option_for_field(self, field):
        return field
