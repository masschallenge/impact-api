# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers.criterion_helper import CriterionHelper


class MatchingIndustryCriterionHelper(CriterionHelper):
    def options(self, spec, apps):
        startups = Startup.objects.filter(application__in=apps)
        top_q = Q(startups__in=startups, parent_id__isnull=True)
        child_q = Q(children__startups__in=startups, parent_id__isnull=True)
        industries = Industry.objects.filter(top_q or child_q).distinct()
        return industries.values_list("name", flat=True)


CriterionHelper.register_helper(MatchingIndustryCriterionHelper,
                                "matching", "industry")
