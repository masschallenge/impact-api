# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from collections import defaultdict
from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingCriterionHelper(CriterionHelper):
    '''Helper for MatchingCriteria. MatchingCriteria specify a parameter on
    which judges and applications should match, for example "All applications
    should be read by at least one judge in the startup's industry".
    Each MatchingCriterion requires exactly one CriterionOptionSpec. The
    `option` field on that spec is ignored, since we are looking for a match
    between two objects, not a specific option.
    A matching criterion's weight and count cannot be set independently for
    different "options", since there are no distinct options.
    '''
    cache_key = ""
    
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
        if not self._app_ids_to_targets and apps.count() > 0:
            self.calc_app_ids_to_targets(apps)
        else:
            self._app_ids_to_targets = {}

    def judge_matches_option(self, judge_data, option):
        return option == judge_data.get(self.judge_field)

    def analysis_fields(self):
        return [
            self.judge_field,
        ]
