# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.judge_criterion_helper import JudgeCriterionHelper
from django.db.models import F


class JudgeGenderCriterionHelper(JudgeCriterionHelper):
    cache_judge_field = "expertprofile__gender"
    judge_field = "judge__" + cache_judge_field

    def analysis_annotate_fields(self):
        return {
            "gender": F(self.judge_field),
        }

    def analysis_tally(self, app_id, db_value, cache):
        gender_value = cache[app_id]["gender"].get(
            db_value["gender"])
        cache[app_id]["gender"][db_value["gender"]] = (
            1 if gender_value is None else gender_value + 1)
