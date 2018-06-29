# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingProgramCriterionHelper(CriterionHelper):
    def app_ids_for_feedback(self, feedbacks, option_name, applications):
        program_family = ProgramFamily.objects.filter(name=option_name).first()
        result = []
        if program_family:
            program_jafs = feedbacks.filter(
                judge__expertprofile__home_program_family=program_family)
            app_pfs = application_program_families(applications)
            for app_id in program_jafs.values_list("application_id", flat=True):
                if app_id in app_pfs and app_pfs[app_id] == program_family.id:
                    result.append(app_id)
        return len(app_pfs), result

    def options(self, spec, apps):
        pfs = ProgramFamily.objects.filter(
            programs__cycle=spec.criterion.judging_round.program.cycle)
        return pfs.values_list("name", flat=True)


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


CriterionHelper.register_helper(MatchingProgramCriterionHelper,
                                "matching", "program")
