# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import Q, F
from mc.models import (
    Industry,
    Startup,
)
from .matching_criterion_helper import MatchingCriterionHelper


class MatchingIndustryCriterionHelper(MatchingCriterionHelper):
    application_field = "startup__primary_industry__id"
    judge_prefix = "judge__"
    cache_judge_field = "expertprofile__primary_industry__name"
    judge_field = judge_prefix + cache_judge_field

    industries = None
    primary_industry_prefix = "application__startup__primary_industry__"
    startup_industry = primary_industry_prefix + "name"
    parent_startup_industry = primary_industry_prefix + "parent__name"

    def __init__(self, subject):
        super().__init__(subject)
        self._top_level_id_cache = None

    def calc_app_ids_to_targets(self, applications):
        top_level_industry_map = compute_top_level_industry_map()
        for app_id, industry_id in applications.values_list(
                "id",
                "startup__primary_industry"):
            top_id, top_name = top_level_industry_map[industry_id]
            self._app_ids_to_targets[app_id] = top_id
            self._target_counts[top_name] = 1 + self._target_counts[top_name]

    def options(self, spec, apps):
        startups = Startup.objects.filter(application__in=apps)
        # Get the top level industry for all applications including
        # those whose industries are direct children of top level
        # industries.
        top_q = Q(startups__in=startups, parent_id__isnull=True)
        child_q = Q(children__startups__in=startups, parent_id__isnull=True)
        industries = Industry.objects.filter(top_q | child_q).distinct()
        return industries.values_list("name", flat=True)

    def option_for_field(self, field):
        return field

    def field_matches_option(self, field, option):
        return self._top_level_id(field) == option

    def _top_level_id(self, field):
        if self._top_level_id_cache is None:
            self._top_level_id_cache = dict(
                list(Industry.objects.filter(
                    parent_id__isnull=True).values_list("id", "name")) +
                list(Industry.objects.filter(
                    parent_id__isnull=False).values_list(
                        "id", "parent__name")))
        return self._top_level_id_cache[field]

    def app_state_analysis_fields(self):
        fields = self.analysis_fields()
        fields + [
            self.startup_industry,
            self.parent_startup_industry,
        ]
        return fields

    def analysis_annotate_fields(self):
        return {
            "judge_industry": F(self.judge_field),
        }

    def get_app_state_criteria_annotate_fields(self):
        fields = self.analysis_annotate_fields()
        fields.update({
            "startup_industry": F(self.startup_industry),
            "primary_startup_industry": F(self.parent_startup_industry),
        })
        return fields

    def analysis_tally(self, app_id, db_value, cache, **kwargs):
        judge_industry = db_value["judge_industry"]
        startup_industry = db_value["startup_industry"]
        primary_startup_industry = db_value["primary_startup_industry"]
        industry_value = cache[app_id]["industry"].get(
            judge_industry)
        if judge_industry in (startup_industry, primary_startup_industry):
            cache[app_id]["industry"][judge_industry] = (
                1 if industry_value is None else industry_value + 1)


def compute_top_level_industry_map():
    top_level_industry_map = {
        industry.id: (industry.parent_id, industry.parent.name)
        for industry in Industry.objects.filter(
            parent_id__isnull=False).prefetch_related('parent')
    }
    top_level_industry_map.update({
        industry.id: (industry.id, industry.name)
        for industry in Industry.objects.filter(parent_id__isnull=True)
    })
    return top_level_industry_map
