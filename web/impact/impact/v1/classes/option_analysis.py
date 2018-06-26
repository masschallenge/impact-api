# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import Counter
from django.db.models import Q
from accelerator.models import (
    Industry,
    JudgeApplicationFeedback,
    ProgramFamily,
    Startup,
    StartupProgramInterest,
)


def app_ids_from_jafs(jafs, **kwargs):
    return jafs.values_list("application_id", flat=True)


def judge_gender(jafs, option_name, **kwargs):
    return app_ids_from_jafs(
        jafs=jafs.filter(judge__expertprofile__gender=option_name[0]))


def judge_role(jafs, option_name, **kwargs):
    return app_ids_from_jafs(
        jafs.filter(judge__expertprofile__expert_category__name=option_name))


def matching_program(jafs, option_name, apps):
    program_family = ProgramFamily.objects.filter(name=option_name).first()
    result = []
    if program_family:
        program_jafs = jafs.filter(
            judge__expertprofile__home_program_family=program_family)
        app_pfs = application_program_families(apps)
        for app_id in program_jafs.values_list("application_id", flat=True):
            if app_id in app_pfs and app_pfs[app_id] == program_family.id:
                result.append(app_id)
    # TODO: Need to return len(app_pfs)
    return len(app_pfs), result


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


def matching_industry(jafs, option_name, apps):
    return app_ids_from_jafs(jafs)


ANALYSIS_REFINEMENTS = {
    ("judge", "gender"): judge_gender,
    ("judge", "role"): judge_role,
    ("matching", "program"): matching_program,
    # ("matching", "industry"): matching_industry,
}


def app_ids_for_existing_feedback(spec, option_name, apps):
    jafs = JudgeApplicationFeedback.objects.filter(
        application__in=apps,
        feedback_status='COMPLETE')
    refinement = ANALYSIS_REFINEMENTS.get((spec.criterion.type,
                                           spec.criterion.name),
                                          app_ids_from_jafs)
    return refinement(jafs=jafs, option_name=option_name, apps=apps)


def all_program_families(spec, *args):
    pfs = ProgramFamily.objects.filter(
        programs__cycle=spec.criterion.judging_round.program.cycle)
    return pfs.values_list("name", flat=True)


def top_level_industries(spec, apps):
    startups = Startup.objects.filter(application__in=apps)
    top_q = Q(startups__in=startups, parent_id__isnull=True)
    child_q = Q(children__startups__in=startups, parent_id__isnull=True)
    industries = Industry.objects.filter(top_q or child_q).distinct()
    return industries.values_list("name", flat=True)


OPTION_FUNCTIONS = {
    ("reads", "reads"): lambda *args: "",
    ("matching", "program"): all_program_families,
    ("matching", "industry"): top_level_industries,
}


class OptionAnalysis(object):
    def __init__(self, option_spec, apps):
        self.option_spec = option_spec
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
        return OPTION_FUNCTIONS[(spec.criterion.type,
                                 spec.criterion.name)](spec, self.apps)

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
        app_ids = app_ids_for_existing_feedback(
            self.option_spec, option_name, self.apps)
        app_counts = Counter(app_ids)
        counts = Counter(app_counts.values())
        unread_count = self.apps.count() - len(app_counts)
        if unread_count != 0:
            counts[0] = unread_count
        expected_count = self.option_spec.count
        return {expected_count - k: v for (k, v) in counts.items()}

    def calc_commitments(self):
        # self.total_commitments = 0
        # self.remaining_commitments = 0
        return {}
