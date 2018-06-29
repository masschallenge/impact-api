# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class JudgeRoleCriterionHelper(CriterionHelper):
    def app_ids_for_feedback(self, feedbacks, option_name, **kwargs):
        return super().app_ids_for_feedback(feedbacks.filter(
            judge__expertprofile__expert_category__name=option_name))


CriterionHelper.register_helper(JudgeRoleCriterionHelper,
                                "judge", "role")
