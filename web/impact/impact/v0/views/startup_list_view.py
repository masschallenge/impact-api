# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from collections import OrderedDict

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from accelerator.models import (
    Startup,
    StartupStatus,
)
from .permissions import (
    V0APIPermissions,
)
from .utils import compose_filter
from ..api_data.startup_list_data import StartupListData
from .utils import (
    BADGE_DISPLAYS,
    base_program_url,
    logo_url,
    status_description,
)


STARTUP_TO_LIST_TAB_ID = [
    "startupstatus",
    "program_startup_status",
    "startup_list_tab_id",
]
STARTUP_TO_PROGRAM = [
    "startupstatus",
    "program_startup_status",
    "program",
]
STARTUP_TO_STATUS_GROUP = [
    "startupstatus",
    "program_startup_status",
    "status_group",
]
STARTUP_IN_STATUSES = ["startupstatus", "program_startup_status", "in"]
STARTUP_TO_STEALTH_STATUS = [
    "startupstatus",
    "program_startup_status",
    "include_stealth_startup_names",
]


class StartupListView(APIView):
    permission_classes = (
        V0APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request):
        self.data = StartupListData(request.data)
        if self.data.valid():
            result = self._calc_result()
            result.update(self._add_status_fields())
            return Response(result)
        return Response(status=404, data=self.data.errors)

    def _add_status_fields(self):
        if self.data.startup_statuses:
            first_pss = self.data.startup_statuses.first()
            return {
                "status": first_pss.startup_list_tab_title,
                "status_description": first_pss.startup_list_tab_description,
                }
        return {}

    def _calc_result(self):
        self.base_url = base_program_url(self.data.program)
        if not self.data.group_by:
            return self._startup_data()
        if self.data.group_by == self.data.INDUSTRY_GROUP_BY:
            return self._industry_group_data()
        elif self.data.group_by.startswith(self.data.STATUS_GROUP_PREFIX):
            return self._status_group_data()

    def _industry_group_data(self):
        startups = self._find_startups().prefetch_related(
            "primary_industry",
            "primary_industry__parent")
        return self._generate_group_data(startups, _top_level_industry)

    def _generate_group_data(self, startups, group_function):
        statuses = self._startups_to_statuses(startups)
        self.groups = OrderedDict()  # Make sure "All" stays first
        for startup in startups:
            description = _startup_description(startup,
                                               statuses.get(startup.id, []),
                                               self.base_url)
            if self.data.all_group == self.data.YES:
                self._add_description(self.data.ALL_INDUSTRY, description)
            self._add_description(group_function(startup), description)
        return self._serialize_groups()

    def _status_group_data(self):
        status_group = self.data.group_by[len(self.data.STATUS_GROUP_PREFIX):]
        startups = self._find_startups().filter(
            **compose_filter(STARTUP_TO_STATUS_GROUP,
                             status_group))
        return self._generate_group_data(startups, lambda _: status_group)

    def _add_description(self, name, description):
        group = self.groups.get(name, [])
        group.append(description)
        self.groups[name] = group

    def _serialize_groups(self):
        groups = []
        for name, startups in self.groups.items():
            groups.append({"group_title": name,
                           "startups": startups})
        return {"groups": groups}

    def _startup_data(self):
        startups = self._find_startups()
        statuses = self._startups_to_statuses(startups)
        return {
            "startups": [_startup_description(startup,
                                              statuses.get(startup.id, []),
                                              self.base_url)
                         for startup in startups]
            }

    def _find_startups(self):
        startups = Startup.objects.filter(
            startupstatus__program_startup_status__program=self.data.program)
        if self.data.startup_statuses:
            startups = startups.filter(
                **compose_filter(STARTUP_IN_STATUSES,
                                 self.data.startup_statuses))
            # The following assumes that if any of the
            # ProgramStartupStatuses in this group are not
            # approved to include stealth startups then
            # stealth startups are excluded.
            if self.data.startup_statuses.filter(
                    include_stealth_startup_names=False):
                startups = startups.exclude(is_visible=False)
        else:
            non_stealth = Q(is_visible=True)
            has_stealth_status = Q(**compose_filter(STARTUP_TO_STEALTH_STATUS,
                                                    True))
            startups = startups.filter(non_stealth | has_stealth_status)
        return self._add_ordering(startups.distinct())

    def _add_ordering(self, startups):
        if self.data.order_by == self.data.RANDOM_ORDER:
            return startups.order_by("?")
        elif self.data.order_by == self.data.ALPHA_DSC_ORDER:
            return startups.order_by("-organization__name")
        return startups.order_by("organization__name")

    def _startups_to_statuses(self, startups):
        statuses = StartupStatus.objects.filter(
            program_startup_status__startup_list_include=True,
            program_startup_status__badge_display__in=BADGE_DISPLAYS,
            startup__in=startups).values_list(
            "startup_id",
            "program_startup_status__startup_status")
        result = {}
        for startup_id, startup_status in statuses:
            item = result.get(startup_id, [])
            item.append(startup_status)
            result[startup_id] = item
        return result


def _startup_description(startup, statuses, base_url):
    if startup.is_visible:
        return {
            "is_visible": True,
            "name": startup.name,
            "id": startup.id,
            "profile_url": base_url + startup.organization.url_slug,
            "logo_url": logo_url(startup),
            "statuses": [status_description(status) for status in statuses],
            }
    else:
        return {
            "is_visible": False,
            "name": startup.name,
            "profile_url": "",
            "logo_url": "",
            "statuses": [],
            }


def _top_level_industry(startup):
    if startup.primary_industry.parent:
        return startup.primary_industry.parent.name
    return startup.primary_industry.name
