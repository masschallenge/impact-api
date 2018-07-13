# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import Counter
from accelerator.models import (
    JudgeApplicationFeedback,
    JudgePanelAssignment,
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
    def __init__(self, option_spec, apps, judging_round):
        self.option_spec = option_spec
        self.judging_round = judging_round
        self.helper = CriterionOptionSpecHelper(option_spec)
        self.apps = apps

    def analyses(self):
        return [self.analysis(option) for option in self.find_options()]

    def analysis(self, option_name):
        result = {
            "criterion_option_spec_id": self.option_spec.id,
            "criterion_name": self.option_spec.criterion.name,
            "option": option_name,
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
        unread_count = (self.helper.app_count(self.apps, option_name) -
                        len(app_counts))
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def all_feedbacks(self):
        scenarios = Scenario.objects.filter(
            judging_round=self.judging_round, is_active=True)
        return JudgeApplicationFeedback.objects.filter(
            application__in=self.apps,
            feedback_status='COMPLETE',
            panel__judgepanelassignment__scenario__in=scenarios)

    def calc_capacity(self, option_name):
        commitments = JudgeRoundCommitment.objects.filter(
            judging_round=self.judging_round)
        total_capacity = self.helper.total_capacity(
            commitments=commitments,
            option_name=option_name)
        assignments = JudgePanelAssignment.objects.filter(
            scenario__judging_round=self.judging_round)
        remaining_capacity = self.helper.remaining_capacity(
            assignments=assignments,
            commitments=commitments,
            option_name=option_name)
        return {
            "total_capacity": total_capacity,
            "remaining_capacity": remaining_capacity,
        }
