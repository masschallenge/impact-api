# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeGenderCriterionHelper(CriterionHelper):
    def app_ids_for_feedback(self, feedbacks, option_name, **kwargs):
        return super().app_ids_for_feedback(
            feedbacks.filter(judge__expertprofile__gender=option_name[0]))
