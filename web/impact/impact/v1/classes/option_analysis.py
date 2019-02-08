# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JudgeApplicationFeedback,
    JudgeRoundCommitment,
    Scenario,
)
from collections import defaultdict
from django.db.models import Sum
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
                                "judge",
                                "gender")
CriterionHelper.register_helper(JudgeRoleCriterionHelper,
                                "judge",
                                "role")
CriterionHelper.register_helper(MatchingIndustryCriterionHelper,
                                "matching",
                                "industry")
CriterionHelper.register_helper(MatchingProgramCriterionHelper,
                                "matching",
                                "program")


class OptionAnalysis(object):
    _judge_to_count = None

    def __init__(self,
                 apps,
                 app_ids,
                 judging_round,
                 application_counts,
                 criterion_helpers):
        self.criterion_helpers = criterion_helpers
        self.judging_round = judging_round
        self.cycle = self.judging_round.program.cycle
        self.apps = apps
        self.app_ids = app_ids
        self.application_counts = application_counts
        self.criterion_total_capacities = {}
        self.judge_capacity_cache = None

        active_scenarios = Scenario.objects.filter(
            judging_round=judging_round, is_active=True)
        self.jpa = JudgeApplicationFeedback.objects.filter(
            application__in=apps,
            panel__judgepanelassignment__scenario__in=active_scenarios)
        self.completed_feedbacks = self.jpa.filter(
            feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE)
        self.application_criteria_read_state_cache = {}

    def analyses(self, option_spec):
        criterion_helper = self.criterion_helpers.get(option_spec.criterion_id)
        spec_helper = CriterionOptionSpecHelper(
            option_spec, self.criterion_helpers)
        options = spec_helper.options(self.apps)
        return [
            self.analysis(option,  criterion_helper, spec_helper)
            for option in options]

    def analysis(self, option_name, helper, spec_helper):
        option_spec = spec_helper.subject
        result = {
            "criterion_option_spec_id": option_spec.id,
            "criterion_name": option_spec.criterion.name,
            "criterion_type": option_spec.criterion.type,
            "criterion_id": option_spec.criterion.id,
            "option": option_name,
            "weight": option_spec.weight,
            "count": option_spec.count,
        }
        result.update(self.calc_needs(option_name, spec_helper))
        result.update(self.calc_capacity(option_name, helper, spec_helper))
        return result

    def calc_needs(self, option_name, spec_helper):
        option_spec = spec_helper.subject
        needs_dist = self.calc_needs_distribution(option_name, spec_helper)
        read_count = option_spec.count
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

    def calc_needs_distribution(self, option_name, spec_helper):
        option_spec = spec_helper.subject
        app_counts = self.application_criteria_read_state(
            self.completed_feedbacks)
        counts = defaultdict(int)
        criterion_name = option_spec.criterion.name
        for count in app_counts.values():
            total = count[criterion_name].get(option_name, 0)
            counts[total] += 1

        read_count = 0
        for count_number in counts:
            if count_number > 0:
                read_count = read_count + counts[count_number]

        unread_count = (
            spec_helper.app_count(self.apps, option_name) - read_count)
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def calc_capacity(self, option_name, helper, spec_helper):
        option_spec = spec_helper.subject
        total_capacity = self.total_capacity(option_name, option_spec)
        remaining_capacity = self.remaining_capacity(self.application_counts,
                                                     option_spec,
                                                     option_name,
                                                     helper)
        return {
            "total_capacity": total_capacity,
            "remaining_capacity": remaining_capacity,
        }

    def populate_criterion_total_capacities_cache(self, field, option_name):
        if self.criterion_total_capacities.get(option_name) is None:
            capacities = JudgeRoundCommitment.objects.filter(
                judging_round=self.judging_round).values(field).annotate(
                    total=Sum("capacity"))
            result = {cap[field]: cap["total"]
                      for cap in capacities}
            self.criterion_total_capacities[option_name] = result

    def total_capacity(self, option, option_spec):
        option_name = option_spec.criterion.name
        helper = self.criterion_helpers[option_spec.criterion.id]
        field = helper.judge_field
        self.populate_criterion_total_capacities_cache(field, option_name)

        key_exists = self.criterion_total_capacities[option_name].get(option)
        return 0 if not key_exists else self.criterion_total_capacities[
            option_name][option]

    def populate_judge_capacity_cache(self):
        if self.judge_capacity_cache is None:
            self.judge_capacity_cache = JudgeRoundCommitment.objects.filter(
                judging_round=self.judging_round).values(
                    *self.get_criteria_fields("judge_id", "capacity")
                ).annotate(
                    **self.get_criteria_annotate_fields()
                )

    def remaining_capacity(self,
                           assignment_counts,
                           option_spec,
                           option,
                           criterion_helper):
        self.populate_judge_capacity_cache()
        return criterion_helper.remaining_capacity(assignment_counts,
                                                   option_spec,
                                                   option,
                                                   self.judge_capacity_cache)

    def get_criteria_fields(self, *args):
        fields = list(args)
        for criterion_helper in self.criterion_helpers.values():
            fields += criterion_helper.analysis_fields()
        return fields

    def get_app_state_criteria_fields(self, *args):
        fields = list(args)
        for criterion_helper in self.criterion_helpers.values():
            fields += criterion_helper.app_state_analysis_fields()
        return fields

    def get_criteria_annotate_fields(self):
        fields = {}
        for criterion_helper in self.criterion_helpers.values():
            fields.update(criterion_helper.analysis_annotate_fields())
        return fields

    def get_app_state_criteria_annotate_fields(self):
        fields = {}
        for criterion_helper in self.criterion_helpers.values():
            fields.update(
                criterion_helper.get_app_state_criteria_annotate_fields())
        return fields

    def application_criteria_read_state(self, feedbacks):
        if not self.application_criteria_read_state_cache:
            ids_cache_value = {}

            db_values = feedbacks.values(
                *self.get_app_state_criteria_fields(
                    "application_id", "judge_id")
            ).annotate(
                **self.get_app_state_criteria_annotate_fields())

            for db_value in db_values:
                app_id = db_value["application_id"]
                if ids_cache_value.get(app_id) is None:
                    ids_cache_value[app_id] = {
                        "industry": {},
                        "program": {},
                        "gender": {},
                        "role": {},
                        "reads": {}
                    }

                for criterion_helper in self.criterion_helpers.values():
                    criterion_helper.analysis_tally(app_id,
                                                    db_value,
                                                    ids_cache_value,
                                                    apps=self.apps)

                self.application_criteria_read_state_cache = ids_cache_value

        return self.application_criteria_read_state_cache


def feedbacks_for_judging_round(judging_round, apps):
    scenarios = Scenario.objects.filter(
        judging_round=judging_round, is_active=True)
    return JudgeApplicationFeedback.objects.filter(
        application__in=apps,
        panel__judgepanelassignment__scenario__in=scenarios)
