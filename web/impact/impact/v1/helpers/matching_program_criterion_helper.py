# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    ProgramFamily,
    Startup,
    StartupProgramInterest,
)
from django.db.models import F
from .matching_criterion_helper import MatchingCriterionHelper


class MatchingProgramCriterionHelper(MatchingCriterionHelper):
    application_field = "startup_id"
    cache_judge_field = "expertprofile__home_program_family__name"
    judge_field = "judge__" + cache_judge_field
    program_families = None

    def __init__(self, subject):
        super().__init__(subject)
        self._program_name_cache = None
        self._app_ids_to_pf_name = {}

    def calc_app_ids_to_targets(self, applications):
        cycle = applications.first().cycle
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
                self._app_ids_to_pf_name[app_id] = pf_name
                self._target_counts[pf_name] += 1

    def options(self, spec, apps):
        pfs = ProgramFamily.objects.filter(
            programs__cycle=spec.criterion.judging_round.program.cycle)
        return pfs.values_list("name", flat=True)

    def option_for_field(self, field):
        return field

    def field_matches_option(self, field, option):
        return self._program_name(field) == option

    def _program_name(self, field):
        if self._program_name_cache is None:
            self._program_name_cache = self._calc_program_name_cache()
        return self._program_name_cache.get(field)

    def _calc_program_name_cache(self):
        cache = {}
        judging_round = self.subject.judging_round
        startups = Startup.objects.filter(
            application__application_type=judging_round.application_type,
            application__application_status="submitted")
        spis = StartupProgramInterest.objects.filter(
            applying=True,
            startup__in=startups).order_by('order').prefetch_related(
                "program__program_family")
        for spi in spis:
            if spi.startup_id not in cache:
                cache[spi.startup_id] = spi.program.program_family.name
        return cache

    def analysis_annotate_fields(self):
        return {"program": F(self.judge_field)}

    def analysis_tally(self, app_id, db_value, cache, **kwargs):
        apps = kwargs.get("apps")
        if not self._app_ids_to_pf_name and apps.count() > 0:
            self.calc_app_ids_to_targets(apps)
        else:
            self._app_ids_to_targets = {}

        program_family = self._app_ids_to_pf_name.get(app_id)
        judge_program = db_value["program"]
        if judge_program == program_family:
            program_value = cache[app_id]["program"].get(judge_program)
            cache[app_id]["program"][judge_program] = (
                1 if program_value is None else program_value + 1)
