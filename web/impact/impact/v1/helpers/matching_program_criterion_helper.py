# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    ProgramFamily,
    StartupProgramInterest,
)
from impact.v1.helpers.matching_criterion_helper import MatchingCriterionHelper


class MatchingProgramCriterionHelper(MatchingCriterionHelper):
    def __init__(self, subject):
        super().__init__(subject)

    def app_ids_for_feedbacks(self, feedbacks, option_name, applications):
        target = ProgramFamily.objects.filter(name=option_name).first()
        return self.find_app_ids(
            self.feedbacks_for_option(feedbacks, option_name),
            applications,
            target)

    def calc_app_ids_to_targets(self, applications):
        app_type = applications.first().application_type
        cycle = app_type.application_type_for.first()
        spi_data = StartupProgramInterest.objects.filter(
            startup__application__in=applications,
            applying=True,
            program__cycle=cycle
        ).order_by("order").values_list("startup_id",
                                        "program__program_family_id",
                                        "program__program_family__name")
        startup_to_app = dict(applications.values_list("startup_id", "id"))
        for startup_id, pf_id, pf_name in spi_data:
            app_id = startup_to_app[startup_id]
            if app_id not in self._app_ids_to_targets:
                self._app_ids_to_targets[app_id] = pf_id
                self._target_counts[pf_name] = self._target_counts.get(pf_name,
                                                                       0) + 1

    def options(self, spec, apps):
        pfs = ProgramFamily.objects.filter(
            programs__cycle=spec.criterion.judging_round.program.cycle)
        return pfs.values_list("name", flat=True)

    def query_for_option(self, query, option_name):
        return query.filter(
            judge__expertprofile__home_program_family__name=option_name)
