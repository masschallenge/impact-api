# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingCriterionHelper(CriterionHelper):
    def __init__(self, subject):
        super().__init__(subject)
        self._app_ids_to_targets = {}
        self._target_counts = {}

    def app_count(self, apps, option_name):
        return self.target_counts(apps).get(option_name, 0)

    def find_app_ids(self, feedbacks, apps, target):
        if not feedbacks:
            return []
        app_map = self.app_ids_to_targets(apps)
        return [app_id for app_id in
                feedbacks.values_list("application_id", flat=True)
                if app_id in app_map and app_map[app_id] == target.id]

    def app_ids_to_targets(self, apps):
        self._check_cache(apps)
        return self._app_ids_to_targets

    def target_counts(self, apps):
        self._check_cache(apps)
        return self._target_counts

    def _check_cache(self, apps):
        if not self._app_ids_to_targets:
            self.calc_app_ids_to_targets(apps)

    @staticmethod
    def instances_by_name(model):
        return {instance.name: instance for instance in model.objects.all()}

    def judge_matches_option(self, judge_data, option):
        return option == judge_data.get(self.judge_field)
