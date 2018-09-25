# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import Counter
from accelerator.models import (
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JudgeApplicationFeedback,
    JudgeRoundCommitment,
    Scenario,
)
from impact.v1.helpers.criterion_option_spec_helper import (
    CriterionOptionSpecHelper,
)
from impact.v1.helpers.criterion_helper import CriterionHelper
from impact.v1.helpers.judge_gender_criterion_helper import (
    JudgeGenderCriterionHelper,
)
from impact.v1.helpers.judge_role_criterion_helper import (
    JudgeRoleCriterionHelper,
)
from impact.v1.helpers.matching_industry_criterion_helper import (
    MatchingIndustryCriterionHelper,
)
from impact.v1.helpers.matching_program_criterion_helper import (
    MatchingProgramCriterionHelper,
)


CriterionHelper.register_helper(JudgeGenderCriterionHelper,
                                "judge", "gender")
CriterionHelper.register_helper(JudgeRoleCriterionHelper,
                                "judge", "role")
CriterionHelper.register_helper(MatchingIndustryCriterionHelper,
                                "matching", "industry")
CriterionHelper.register_helper(MatchingProgramCriterionHelper,
                                "matching", "program")


class OptionAnalysis(object):
    _judge_to_count = None

    def __init__(self,
                 option_spec,
                 apps,
                 app_ids,
                 judging_round,
                 application_counts):
        self.option_spec = option_spec
        self.judging_round = judging_round
        self.helper = CriterionOptionSpecHelper(option_spec)
        self.apps = apps
        self.app_ids = app_ids
        self.application_counts = application_counts

    def analyses(self):
        return [self.analysis(option) for option in self.find_options()]

    def analysis(self, option_name):
        result = {
            "criterion_option_spec_id": self.option_spec.id,
            "criterion_name": self.option_spec.criterion.name,
            "criterion_type": self.option_spec.criterion.type,
            "criterion_id": self.option_spec.criterion.id,
            "option": option_name,
            "weight": self.option_spec.weight,
            "count": self.option_spec.count,
        }
        result.update(self.calc_needs(option_name))
        result.update(self.calc_capacity(option_name))
        return result

    def find_options(self):
        spec = self.option_spec
        if spec.option:
            return [spec.option]
        return self.helper.options(self.apps)

    def calc_needs(self, option_name):
        needs_dist = self.calc_needs_distribution(option_name)
        read_count = self.option_spec.count
        return {
            "needs_distribution": needs_dist,
            "total_required_reads": read_count * sum(needs_dist.values()),
            "completed_required_reads": sum(
                [min(read_count, read_count - k) * v
                 for (k, v) in needs_dist.items()]),
            "satisfied_apps": sum(
                [v for (k, v) in needs_dist.items() if k <= 0]),
            "needy_apps": sum(
                [v for (k, v) in needs_dist.items() if k > 0]),
            "remaining_needed_reads": sum(
                [v*k for (k, v) in needs_dist.items() if k > 0])
        }

    def calc_needs_distribution(self, option_name):
        app_ids = self.helper.app_ids_for_feedbacks(self.completed_feedbacks(),
                                                    option_name=option_name,
                                                    applications=self.apps)
        app_counts = Counter(app_ids)
        counts = Counter(app_counts.values())
        unread_count = (self.helper.app_count(self.apps, option_name) -
                        len(app_counts))
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def completed_feedbacks(self):
        return feedbacks_for_judging_round(
            self.judging_round, self.apps).filter(
                feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE)

    def calc_capacity(self, option_name):
        commitments = JudgeRoundCommitment.objects.filter(
            judging_round=self.judging_round)
        total_capacity = self.helper.total_capacity(
            commitments=commitments,
            option_name=option_name)
        remaining_capacity = self.helper.remaining_capacity(
            commitments,
            self.application_counts,
            option_name)
        return {
            "total_capacity": total_capacity,
            "remaining_capacity": remaining_capacity,
        }


def feedbacks_for_judging_round(judging_round, apps):
    scenarios = Scenario.objects.filter(
        judging_round=judging_round, is_active=True)
    return JudgeApplicationFeedback.objects.filter(
        application__in=apps,
        panel__judgepanelassignment__scenario__in=scenarios)
