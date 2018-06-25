# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import Counter
from accelerator.models import (
    Application,
    JudgeApplicationFeedback,
    StartupProgramInterest,
)


def app_ids_from_jafs(jafs, **kwargs):
    return jafs.values_list("application_id", flat=True)


def judge_gender(jafs, option, **kwargs):
    return app_ids_from_jafs(
        jafs=jafs.filter(judge__expertprofile__gender=option[0]))


def judge_role(jafs, option, **kwargs):
    return app_ids_from_jafs(
        jafs.filter(judge__expertprofile__expert_category__name=option))


def matching_program(jafs, option, apps):
    app_pfs = application_program_families(apps)
    result = []
    for (app_id, judge_id, pf_id) in jafs.values_list(
            "application_id",
            "judge_id",
            "judge__expertprofile__home_program_family_id"):
        if app_id in app_pfs and app_pfs[app_id] == pf_id:
            result.append(app_id)
    return result


def application_program_families(apps):
    spi_data = StartupProgramInterest.objects.filter(
        startup__application__in=apps, applying=True
    ).order_by("order").values_list("startup_id",
                                    "program__program_family_id")
    startup_to_app = dict(apps.values_list("startup_id", "id"))
    app_to_pf = {}
    for startup_id, pf_id in spi_data:
        app_id = startup_to_app[startup_id]
        if app_id not in app_to_pf:
            app_to_pf[app_id] = pf_id
    return app_to_pf


def matching_industry(jafs, option, apps):
    return app_ids_from_jafs(jafs)


ANALYSIS_REFINEMENTS = {
    ("judge", "gender"): judge_gender,
    ("judge", "role"): judge_role,
    ("matching", "program"): matching_program,
    # ("matching", "industry"): matching_industry,
}


def app_ids_for_existing_feedback(spec, apps):
    jafs = JudgeApplicationFeedback.objects.filter(
        application__in=apps,
        feedback_status='COMPLETE')
    refinement = ANALYSIS_REFINEMENTS.get((spec.criterion.type,
                                           spec.criterion.name),
                                          app_ids_from_jafs)
    return refinement(jafs=jafs, option=spec.option, apps=apps)


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
        app_ids = app_ids_for_existing_feedback(self.option_spec, apps)
        app_counts = Counter(app_ids)
        counts = Counter(app_counts.values())
        unread_count = apps.count() - len(app_counts)
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def calc_commitments(self):
        self.total_commitments = 0
        self.remaining_commitments = 0
