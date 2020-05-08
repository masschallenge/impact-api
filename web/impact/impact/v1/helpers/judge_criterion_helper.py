# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import F
from .v1.helpers.criterion_helper import CriterionHelper


class JudgeCriterionHelper(CriterionHelper):
    '''Helper for JudgeCriteria. JudgeCriteria specify a feature which
    all applications are "looking for", for example "All startups should be
    read by at least one female judge".
    JudgeCriteria require one CriterionOptionSpec for each feature sought, for
    example, "one female judge and one male judge" would require two
    OptionSpecs. Weight and count can be set independently for each option.
    '''

    def option_for_field(self, field):
        return field

    def judge_matches_option(self, judge_data, option):
        return option == judge_data.get(self.cache_key)

    def analysis_fields(self):
        return [
            self.judge_field,
        ]

    def analysis_annotate_fields(self):
        return {
            self.cache_key: F(self.judge_field),
            }
