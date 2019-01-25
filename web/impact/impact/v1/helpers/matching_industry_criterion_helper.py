# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import Q
from accelerator.models import (
    Industry,
    Startup,
)
from impact.v1.helpers.matching_criterion_helper import MatchingCriterionHelper


class MatchingIndustryCriterionHelper(MatchingCriterionHelper):
    application_field = "startup__primary_industry__id"
    judge_field = "expertprofile__primary_industry__name"
    industries = None

    def __init__(self, subject):
        super().__init__(subject)
        self._top_level_id_cache = None

    def _industry_map(self):
        if self.industries is None:
            self.industries = self.instances_by_name(Industry)
        return self.industries

    def app_ids_for_feedbacks(self, feedbacks, option_name, applications):
        target = self._industry_map()[option_name]
        return self.find_app_ids(
            self.filter_by_judge_option(feedbacks, option_name),
            self.app_ids_to_targets(applications),
            target)

    def calc_app_ids_to_targets(self, applications):
        top_level_industry_map = {
            industry.id: (industry.parent_id, industry.parent.name)
            for industry in Industry.objects.filter(
                    parent_id__isnull=False).prefetch_related('parent')
        }
        top_level_industry_map.update({
            industry.id: (industry.id, industry.name)
            for industry in Industry.objects.filter(parent_id__isnull=True)
        })
        for app_id, industry_id in applications.values_list(
                "id", "startup__primary_industry"):
            top_id, top_name = top_level_industry_map[industry_id]
            self._app_ids_to_targets[app_id] = top_id
            self._target_counts[top_name] = self._target_counts.get(top_name,
                                                                    0) + 1

    def options(self, spec, apps):
        startups = Startup.objects.filter(application__in=apps)
        # Get the top level industry for all applications including
        # those whose industries are direct children of top level
        # industries.
        top_q = Q(startups__in=startups, parent_id__isnull=True)
        child_q = Q(children__startups__in=startups, parent_id__isnull=True)
        industries = Industry.objects.filter(top_q | child_q).distinct()
        return industries.values_list("name", flat=True)

    def filter_by_judge_option(self, query, option_name):
        return query.filter(
            judge__expertprofile__primary_industry__name=option_name)

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
