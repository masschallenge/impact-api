# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import Counter
from django.db.models import (
    Case,
    Count,
    Q,
    When,
)

from accelerator.models import (
    Application,
    JudgeApplicationFeedback,
)


class OptionAnalysis(object):
    def __init__(self, option_spec):
        self.option_spec = option_spec

    def analysis(self):
        self.calc_needs()
        self.calc_commitments()
        return {
            "criterion_option_spec_id": self.option_spec.id,
            "criterion_name": self.option_spec.criterion.name,
            "option": self.option_spec.option,
            "total_required_reads": self.total_required_reads,
            "needs_distribution": self.needs_distribution,
            "satisfied_apps": self.satisfied_apps,
            "needy_apps": self.needy_apps,
            "remaining_needed_reads": self.remaining_needed_reads,
            "total_commitments": self.total_commitments,
            "remaining_commitments": self.remaining_commitments,
        }

    def calc_needs(self):
        needs_dist = self.calc_needs_distribution()
        self.needs_distribution = needs_dist
        self.total_required_reads = self.option_spec.count * sum(
            needs_dist.values())
        self.satisfied_apps = sum(
            [v for (k, v) in needs_dist.items() if k <= 0])
        self.needy_apps = sum(
            [v for (k, v) in needs_dist.items() if k > 0])
        self.remaining_needed_reads = sum(
            [v*k for (k, v) in needs_dist.items() if k > 0])

    def calc_needs_distribution(self):
        judging_round = self.option_spec.criterion.judging_round
        apps = Application.objects.filter(
            application_status="submitted",
            application_type=judging_round.application_type)
        app_ids = JudgeApplicationFeedback.objects.filter(
            application__in=apps,
            feedback_status='COMPLETE').values_list("application_id",
                                                    flat=True)
        app_counts = Counter(app_ids)
        counts = Counter(app_counts.values())
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def calc_commitments(self):
        self.total_commitments = 0
        self.remaining_commitments = 0

