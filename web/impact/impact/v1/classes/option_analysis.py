# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import Counter
from accelerator.models import JudgeApplicationFeedback
from impact.v1.helpers.criterion_option_spec_helper import (
    CriterionOptionSpecHelper,
)


class OptionAnalysis(object):
    def __init__(self, option_spec, apps):
        self.option_spec = option_spec
        self.helper = CriterionOptionSpecHelper(option_spec)
        self.apps = apps

    def analyses(self):
        return [self.analysis(name) for name in self.find_options()]

    def analysis(self, option_name):
        result = {
            "criterion_option_spec_id": self.option_spec.id,
            "criterion_name": self.option_spec.criterion.name,
            "option": option_name,
        }
        result.update(self.calc_needs(option_name))
        result.update(self.calc_commitments())
        return result

    def find_options(self):
        spec = self.option_spec
        if spec.option:
            return [spec.option]
        return self.helper.optionsXYZ(self.apps)

    def calc_needs(self, option_name):
        needs_dist = self.calc_needs_distribution(option_name)
        return {
            "needs_distribution": needs_dist,
            "total_required_reads": self.option_spec.count * sum(
                needs_dist.values()),
            "satisfied_apps": sum(
                [v for (k, v) in needs_dist.items() if k <= 0]),
            "needy_apps": sum(
                [v for (k, v) in needs_dist.items() if k > 0]),
            "remaining_needed_reads": sum(
                [v*k for (k, v) in needs_dist.items() if k > 0])
        }

    def calc_needs_distribution(self, option_name):
        app_ids = self.helper.app_ids_for_feedback(self.all_feedbacks(),
                                                   option_name=option_name,
                                                   applications=self.apps)
        app_counts = Counter(app_ids)
        counts = Counter(app_counts.values())
        unread_count = self.apps.count() - len(app_counts)
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def all_feedbacks(self):
        return JudgeApplicationFeedback.objects.filter(
            application__in=self.apps,
            feedback_status='COMPLETE')

    def calc_commitments(self):
        # self.total_commitments = 0
        # self.remaining_commitments = 0
        return {}
