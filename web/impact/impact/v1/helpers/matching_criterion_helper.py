# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from collections import defaultdict
from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingCriterionHelper(CriterionHelper):
    def __init__(self, subject):
        super().__init__(subject)
        self._app_ids_to_targets = {}
        self._target_counts = defaultdict(int)

    def app_count(self, apps, option_name):
        return self.target_counts(apps).get(option_name, 0)

    def target_counts(self, apps):
        self._check_cache(apps)
        return self._target_counts

    def _check_cache(self, apps):
        if not self._app_ids_to_targets:
            self.calc_app_ids_to_targets(apps)

    def judge_matches_option(self, judge_data, option):
        return option == judge_data.get(self.judge_field)

    def analysis_fields(self):
        return [
            self.judge_field,
        ]
