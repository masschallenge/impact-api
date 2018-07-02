# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    ProgramFamily,
    StartupProgramInterest,
)
from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingProgramCriterionHelper(CriterionHelper):
    def __init__(self, subject):
        super().__init__(subject)
        self.app_ids_to_program_families = {}
        self.pf_counts = {}

    def app_ids_for_feedback(self, feedbacks, option_name, applications):
        program_family = ProgramFamily.objects.filter(name=option_name).first()
        result = []
        if program_family:
            program_jafs = feedbacks.filter(
                judge__expertprofile__home_program_family=program_family)
            app_pfs = self.application_program_families(applications)
            for app_id in program_jafs.values_list("application_id",
                                                   flat=True):
                if app_id in app_pfs and app_pfs[app_id] == program_family.id:
                    result.append(app_id)
        return result

    def options(self, spec, apps):
        pfs = ProgramFamily.objects.filter(
            programs__cycle=spec.criterion.judging_round.program.cycle)
        return pfs.values_list("name", flat=True)

    def app_count(self, apps, option_name):
        return self.program_family_counts(apps).get(option_name, 0)

    def application_program_families(self, apps):
        if not self.app_ids_to_program_families:
            self.calc_app_ids_to_program_families(apps)
        return self.app_ids_to_program_families

    def program_family_counts(self, apps):
        if not self.app_ids_to_program_families:
            self.calc_app_ids_to_program_families(apps)
        return self.pf_counts

    def calc_app_ids_to_program_families(self, apps):
        cycle = apps.first().application_type.application_type_for.first()
        spi_data = StartupProgramInterest.objects.filter(
            startup__application__in=apps,
            applying=True,
            program__cycle=cycle
        ).order_by("order").values_list("startup_id",
                                        "program__program_family_id",
                                        "program__program_family__name")
        startup_to_app = dict(apps.values_list("startup_id", "id"))
        for startup_id, pf_id, pf_name in spi_data:
            app_id = startup_to_app[startup_id]
            if app_id not in self.app_ids_to_program_families:
                self.app_ids_to_program_families[app_id] = pf_id
                self.pf_counts[pf_name] = self.pf_counts.get(pf_name, 0) + 1
