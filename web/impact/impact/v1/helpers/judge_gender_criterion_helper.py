# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from django.db.models import F
from collections import defaultdict

from mc_apply.reports.concat import Concat
from .judge_criterion_helper import JudgeCriterionHelper


class JudgeGenderCriterionHelper(JudgeCriterionHelper):
    cache_judge_field = "expertprofile__gender_identity__name"
    judge_field = "judge__" + cache_judge_field
    cache_key = cache_judge_field

    def analysis_annotate_fields(self):
        return {
            "gender": F(self.judge_field),
            self.cache_key: F(self.judge_field)
        }

    def analysis_tally(self, app_id, db_value, cache, **kwargs):
        gender_dict = defaultdict(lambda: "o")
        gender_dict.update({"Female": 'f',"Male": 'm'})
        db_value["gender"] = gender_dict[db_value["gender"]]
        db_value[self.cache_judge_field] = db_value["gender"]
        db_value[self.judge_field] = db_value["gender"]
        gender_value = cache[app_id]["gender"].get(
            db_value["gender"])
        cache[app_id]["gender"][db_value["gender"]] = (
            1 if gender_value is None else gender_value + 1)
