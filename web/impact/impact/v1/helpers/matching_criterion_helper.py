# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import Q
from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingCriterionHelper(CriterionHelper):
    def __init__(self, subject):
        super().__init__(subject)
        self._app_ids_to_targets = {}
        self._target_counts = {}

    def app_count(self, apps, option_name):
        return self.target_counts(apps).get(option_name, 0)

    def refine_feedbacks(self, feedbacks, target, refinement):
        if not target:
            return None
        query = Q(**{refinement: target})
        return feedbacks.filter(query)

    def find_app_ids(self, feedbacks, apps, target):
        result = []
        if feedbacks:
            app_map = self.app_ids_to_targets(apps)
            for app_id in feedbacks.values_list("application_id", flat=True):
                if app_id in app_map and app_map[app_id] == target.id:
                    result.append(app_id)
        return result

    def app_ids_to_targets(self, apps):
        if not self._app_ids_to_targets:
            self.calc_app_ids_to_targets(apps)
        return self._app_ids_to_targets

    def target_counts(self, apps):
        if not self._app_ids_to_targets:
            self.calc_app_ids_to_targets(apps)
        return self._target_counts
