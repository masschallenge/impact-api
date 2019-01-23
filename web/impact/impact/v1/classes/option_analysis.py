# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JudgeApplicationFeedback,
    JudgeRoundCommitment,
    Scenario,
)
from django.db.models import Sum, F, Count
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
from accelerator_abstract.models.base_core_profile import (
    UI_GENDER_CHOICES
)

CriterionHelper.register_helper(
    JudgeGenderCriterionHelper, "judge", "gender")
CriterionHelper.register_helper(
    JudgeRoleCriterionHelper, "judge", "role")
CriterionHelper.register_helper(
    MatchingIndustryCriterionHelper, "matching", "industry")
CriterionHelper.register_helper(
    MatchingProgramCriterionHelper, "matching", "program")


class OptionAnalysis(object):
    _judge_to_count = None
    expert_profile = "judge__expertprofile__"
    industry_judge_field = expert_profile + "primary_industry__name"
    program_judge_field = expert_profile + "home_program_family__name"
    gender_judge_field = expert_profile + "gender"
    role_judge_field = expert_profile + "expert_category__name"

    def __init__(self,
                 apps,
                 app_ids,
                 judging_round,
                 application_counts,
                 criterion_helpers):
        self.criterion_helpers = criterion_helpers
        self.option_spec = None
        self.judging_round = judging_round
        self.cycle = self.judging_round.program.cycle
        self.helper = None
        self.apps = apps
        self.app_ids = app_ids
        self.application_counts = application_counts
        self.criterion_total_capacities = {}
        self.judge_to_capacity_cache = None
        self.criterion_total_functions = {
            ("judge", "gender"): {
                'function': self.general_criterion_total_capacity,
                'filter_field': self.gender_judge_field,
            },
            ("reads", "reads"): {
                'function': None,
            },
            ("judge", "role"): {
                'function': self.general_criterion_total_capacity,
                'filter_field': self.role_judge_field,
            },
            ("matching", "industry"): {
                'function': self.general_criterion_total_capacity,
                'filter_field': self.industry_judge_field,
            },
            ("matching", "program"): {
                'function': self.general_criterion_total_capacity,
                'filter_field': self.program_judge_field,
            }
        }
        active_scenarios = Scenario.objects.filter(
            judging_round=judging_round, is_active=True)
        self.jpa = JudgeApplicationFeedback.objects.filter(
            application__in=apps,
            panel__judgepanelassignment__scenario__in=active_scenarios)
        self.app_ids_for_feedbacks_cache = {}
        self.gender_match_dict = dict(
            (value.lower(), key) for key, value in UI_GENDER_CHOICES)

    def analyses(self, option_spec):
        self.option_spec = option_spec
        self.helper = CriterionOptionSpecHelper(
            option_spec, self.criterion_helpers)
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
        app_counts = self.app_ids_for_feedbacks(
            self.completed_feedbacks(),
            option_name=option_name,
            applications=self.apps)
        counts = {}
        for count in app_counts:
            total = count["total"]
            counts[total] = (
                1 if counts.get(total) is None else counts[total] + 1)

        read_count = 0
        for count_number in counts:
            if count_number > 0:
                read_count = read_count + counts[count_number]

        unread_count = (
            self.helper.app_count(self.apps, option_name) - read_count)
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def completed_feedbacks(self):
        return self.jpa.filter(
            feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE)

    def calc_capacity(self, option_name):
        commitments = JudgeRoundCommitment.objects.filter(
            judging_round=self.judging_round)
        criteria_function = self.criterion_total_functions[
            (self.option_spec.criterion.type, self.option_spec.criterion.name)
        ]['function']
        total_capacity = (
            criteria_function(option_name)
            if criteria_function is not None
            else self.helper.total_capacity(
                commitments=commitments,
                option_name=option_name)
        )
        remaining_capacity = self.remaining_capacity(
            self.application_counts,
            self.option_spec,
            option_name)
        return {
            "total_capacity": total_capacity,
            "remaining_capacity": remaining_capacity,
        }

    def general_criterion_total_capacity(self, option):
        option_name = self.option_spec.criterion.name
        field = self.criterion_total_functions[
            (self.option_spec.criterion.type, option_name)
        ]['filter_field']

        if option_name == "gender":
            option = self.gender_match_dict[option]

        if self.criterion_total_capacities.get(option_name) is None:
            capacities = JudgeRoundCommitment.objects.filter(
                judging_round=self.judging_round) \
                .values(field) \
                .annotate(total=Sum("capacity"))
            result = {
                cap[field]: cap["total"]
                for cap in capacities}
            self.criterion_total_capacities[option_name] = result

        key_exists = self.criterion_total_capacities[option_name].get(option)
        return 0 if not key_exists else self.criterion_total_capacities[
            option_name][option]

    def remaining_capacity(self, assignment_counts, option_spec, option):
        if self.judge_to_capacity_cache is None:
            self.judge_to_capacity_cache = JudgeRoundCommitment.objects.filter(
                judging_round=self.judging_round).values(
                    "judge_id",
                    self.industry_judge_field,
                    self.program_judge_field,
                    self.gender_judge_field,
                    self.role_judge_field,
                    "capacity"
                ).annotate(
                    industry=F(self.industry_judge_field),
                    program=F(self.program_judge_field),
                    gender=F(self.gender_judge_field),
                    role=F(self.role_judge_field),
                )

        result = 0
        option_name = option_spec.criterion.name

        for judge in self.judge_to_capacity_cache:
            gender_option = 'prefer not to state'
            if option_name == "gender":
                gender_option = self.gender_match_dict[option]

            if (
                option_name == "reads" or
                judge[option_name] == option or
                judge[option_name] == gender_option
            ):
                result += max(0, judge['capacity'] - assignment_counts.get(
                    judge['judge_id'], 0))
        return result

    def app_ids_for_feedbacks(self, feedbacks, option_name, **kwargs):
        criterion_name = self.option_spec.criterion.name
        criterion_type = self.option_spec.criterion.type

        key = (criterion_type, criterion_name, option_name)

        if criterion_name == "gender":
            option_name = self.gender_match_dict[option_name]

        ids_cache_value = self.app_ids_for_feedbacks_cache.get(key)
        if ids_cache_value is None:
            ids_cache_value = self.filter_by_judge_option(
                feedbacks, option_name).values(
                    "application_id").annotate(total=Count('application_id'))
        return ids_cache_value

    def filter_by_judge_option(self, query, option_name):

        if self.option_spec.criterion.name == "reads":
            return query

        field = self.criterion_total_functions[
            (self.option_spec.criterion.type, self.option_spec.criterion.name)
        ]['filter_field']
        return query.filter(**{field: option_name})


def feedbacks_for_judging_round(judging_round, apps):
    scenarios = Scenario.objects.filter(
        judging_round=judging_round, is_active=True)
    return JudgeApplicationFeedback.objects.filter(
        application__in=apps,
        panel__judgepanelassignment__scenario__in=scenarios)
