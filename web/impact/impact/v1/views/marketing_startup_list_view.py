import json
import logging

from collections import OrderedDict as odict
from Cryptodome.Cipher import AES
from django.conf import settings
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
)
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
from time import time

from accelerator_abstract.models.base_program_startup_status import (
    BADGE_STARTUP_LIST,
    BADGE_STARTUP_LIST_AND_PROFILE,
    BADGE_STARTUP_PROFILE,
)
from accelerator.models import (
    Industry,
    ProgramStartupStatus,
    Site,
    SiteProgramAuthorization,
    Startup,
    StartupStatus,
    StartupTeamMember,
)
from impact.v1.views.impact_view import ImpactView
from impact.v1.views.utils import (
    get_image_token,
    status_dict,
    status_displayable,
)
from impact.v1.views.utils import pad


class MarketingStartupListView(ImpactView):
    view_name = "marketing_startup_list_view"

    def __init__(self):
        self.acceptable_badge_display = (
            BADGE_STARTUP_PROFILE, BADGE_STARTUP_LIST_AND_PROFILE)
        self.status_groups = odict()
        self.data = {}
        self.startups = []
        self.already_listed_startups = {}
        self.industry_startup_ids = odict([(
            industry.name, []) 
            for industry in Industry.objects.filter(parent=None
            ).order_by('name').all()])
        self.is_public = {}
        self.stealth_still_listed = {}

    def get(self, request):
        query = StartupStatus.objects.filter(
            program_startup_status__program__name__in=request.GET.getlist(
                'program_key'),
            program_startup_status__startup_list_include=True)
        query = query.order_by(
            'startup__organization__name',
            'program_startup_status__sort_order',
            'program_startup_status__startup_status')
        site = Site.objects.get(name=request.GET['site_name'])
        profile_urls = self.get_base_profile_url(
            request.GET.getlist('program_key'), query, site)
        self.get_startups(query, profile_urls, site)
        self.badge_display(query)
        if 'group_by' in list(request.GET):
            key = request.GET.get('group_by').lower()
            self.group_startups(key)
            if request.GET.get('include_all_group', 'Y') != 'N':
                self.data["groups"] = [{
                    'group_title': 'All',
                    'startups': self.startups}, ] + self.data["groups"]
        else:
            self.data["startups"] = self.startups
        return HttpResponse(json.dumps(self.data), content_type="application/json")

    def get_base_profile_url(self, program_names, query, site):
        base_url = ''
        for spa in SiteProgramAuthorization.objects.filter(
                site=site, program__name__in=program_names):
            if spa.startup_profile_base_url:
                base_url = spa.startup_profile_base_url
                break
        base_url = base_url + '/' if base_url[-1] != '/' else base_url
        profile_urls = dict([(ss.startup_id,
                          base_url + ss.startup.organization.url_slug)
                         for ss in query.select_related('startup')
                         if ss.startup.is_visible])
        return profile_urls

    def get_public_startups(self, startup, startup_status, profile_urls):
        self.is_public[startup.id] = True
        industry = startup.primary_industry.parent.name if (
            startup.primary_industry.parent
        ) else startup.primary_industry.name
        self.industry_startup_ids[industry].append(startup.id)
        self.already_listed_startups[startup.id] = len(self.startups)
        self.startups.append({
            'name': startup.name,
            'is_visible': startup.is_visible,
            'profile_url': profile_urls[startup.id],
            'logo_url': (startup.high_resolution_logo.url if
                        startup.high_resolution_logo else ''),
            'image_token': get_image_token(
                startup.high_resolution_logo.name) if (
                startup.high_resolution_logo) else '',
            'statuses': [
                status_dict(startup_status),
            ] if status_displayable(startup_status,
            self.status_groups, self.acceptable_badge_display) else [],
        })
        if self.startups[-1]['statuses']:
            self.status_groups[(
                startup_status.startup_id,
                startup_status.program_startup_status.status_group)
            ] = startup_status.program_startup_status.startup_status

    def get_non_public_startups(self, startup, startup_status):
        self.is_public[startup.id] = False
        pstatus = startup_status.program_startup_status
        if pstatus.include_stealth_startup_names:
            self.stealth_still_listed[startup.id] = True
            industry = startup.primary_industry.parent.name if (
                startup.primary_industry.parent
            ) else startup.primary_industry.name
            self.industry_startup_ids[industry].append(startup.id)
            self.already_listed_startups[startup.id] = len(self.startups)
            self.startups.append({
                'name': startup.name,
                'is_visible': False,
                'profile_url': '',
                'logo_url': '',
                'image_token': '',
                'statuses': [],
            })
        else:
            self.stealth_still_listed[startup.id] = False

    def create_startup_record(self, startup, startup_status):
        if self.is_public[startup.id]:
            if status_displayable(startup_status,
            self.status_groups, self.acceptable_badge_display):
                self.startups[
                    self.already_listed_startups[
                        startup_status.startup.id]]['statuses'].append(
                            status_dict(startup_status))
                self.status_groups[(
                    startup_status.startup_id,
                    startup_status.program_startup_status.status_group
                    )] = startup_status.program_startup_status.startup_status

    def get_startups(self, query, profile_urls, site):
        for startup_status in query.select_related(
                'startup',
                'startup__primary_industry',
                'program_startup_status',
                'startup__primary_industry__parent').all():
            startup = startup_status.startup

            if startup.id in self.already_listed_startups:
                self.create_startup_record(startup, startup_status)
            else:
                if startup.is_visible:
                    self.get_public_startups(startup, startup_status, profile_urls)
                else:
                    self.get_non_public_startups(startup, startup_status)

    def badge_display(self, query):
        pfilter = {
            'program_startup_status__badge_display__in': self.acceptable_badge_display
        }
        for leftover_startup_status in StartupStatus.objects.filter(
                startup_id__in=list(self.already_listed_startups.keys())
        ).filter(**pfilter).exclude(
            program_startup_status__status_group__in=self.status_groups
        ).exclude(id__in=[ss.id for ss in query.all()]).select_related(
            'program_startup_status',
        ).all():
            self.startups[self.already_listed_startups[leftover_startup_status.startup.id]][
                'statuses'].append(status_dict(leftover_startup_status))

    def group_startups(self, key):
        if key == 'industry':
            self.data["groups"] = [{
                'group_title': industry_name,
                'startups': [
                    self.startups[
                        self.already_listed_startups[startup_id]
                    ] for startup_id in ids]} for
                industry_name, ids in list(self.industry_startup_ids.items())]
        elif key.startswith('statusgroup:'):
            groupname = key.split(':')[1]
            groups = {}
            for (startup_id, status_group), status in self.status_groups.items():
                if status_group == groupname:
                    startup = self.startups[self.already_listed_startups[startup_id]]
                    if status in groups:
                        groups[status].append(startup)
                    else:
                        groups[status] = [startup, ]
            self.data['groups'] = [{'group_title': k, 'startups': v}
                            for k, v in list(groups.items())]
        else:
            raise Exception(
                "group_by param {0} not valid".format(key))