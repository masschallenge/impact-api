# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.judge_criterion_helper import JudgeCriterionHelper
from django.db.models import F


class JudgeRoleCriterionHelper(JudgeCriterionHelper):
    cache_judge_field = "expertprofile__expert_category__name"
    judge_field = "judge__" + cache_judge_field

    def analysis_annotate_fields(self):
        return {
            "role": F(self.judge_field),
        }

    def analysis_tally(self, app_id, db_value, cache, **kwargs):
        role_value = cache[app_id]["role"].get(
            db_value["role"])
        cache[app_id]["role"][db_value["role"]] = (
            1 if role_value is None else role_value + 1)
