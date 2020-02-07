import base64
import hashlib
import json
import logging

import os
import re
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
from impact.v1.views.utils import pad


class MarketingStartupListView(ImpactView):
    view_name = "marketing_startup_list_view"

    def __init__(self):
        self.acceptable_badge_display = (
            BADGE_STARTUP_PROFILE, BADGE_STARTUP_LIST_AND_PROFILE)
        self.status_groups = odict()

    def get_image_token(self, name):
        # Create initialization vector,
        # servicekey and encryption object for creating image_token
        #  the service key is a hash of the password from the settings file,
        # we use the first 32 bytes as 32 is
        #  a key length restriction.
        iv = os.urandom(settings.IMAGE_TOKEN_BLOCK_SIZE)
        servicekey = hashlib.sha256(
            settings.IMAGE_TOKEN_PASSWORD.encode()).hexdigest()[:32]
        aes = AES.new(servicekey.encode(), AES.MODE_CBC, iv)
        raw = pad(name + ":" + str(time())).encode()[:32]
        # We .decode() return value because json.dumps needs str values, not bytes
        return base64.urlsafe_b64encode((iv + aes.encrypt(raw))).decode()

    def status_dict(self, startup_status):
        return {
            'status_name': startup_status.program_startup_status.startup_status,
            'status_badge_url': (
                startup_status.program_startup_status.badge_image.url
            )
            if startup_status.program_startup_status.badge_image else '',
            'status_badge_token': self.get_image_token(
                startup_status.program_startup_status.badge_image.name
            ) if startup_status.program_startup_status.badge_image else '',
        }

    def status_displayable(self, startup_status):
        pstatus = startup_status.program_startup_status
        return (
            not startup_status.program_startup_status.status_group or (
                startup_status.startup_id,
                startup_status.program_startup_status.status_group
            ) not in self.status_groups
        ) and (pstatus.badge_display in self.acceptable_badge_display)

    def get(self, request):
        program_names = request.GET.getlist('program_key')
        site_name = request.GET['site_name']
        query = StartupStatus.objects.filter(
            program_startup_status__program__name__in=program_names,
            program_startup_status__startup_list_include=True)
        data = {}
        query = query.order_by(
            'startup__organization__name',
            'program_startup_status__sort_order',
            'program_startup_status__startup_status')
        startups = []
        already_listed_startups = {}
        industry_startup_ids = odict([(
            industry.name, []) 
            for industry in Industry.objects.filter(parent=None
            ).order_by('name').all()])
        is_public = {}
        stealth_still_listed = {}
        site = Site.objects.get(name=site_name)
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
        for startup_status in query.select_related(
                'startup',
                'startup__primary_industry',
                'program_startup_status',
                'startup__primary_industry__parent').all():
            startup = startup_status.startup

            if startup.id in already_listed_startups:
                if is_public[startup.id]:
                    if self.status_displayable(startup_status):
                        startups[
                            already_listed_startups[
                                startup_status.startup.id]]['statuses'].append(
                            self.status_dict(startup_status))
                        self.status_groups[(
                            startup_status.startup_id,
                            startup_status.program_startup_status.status_group
                        )] = startup_status.program_startup_status.startup_status
            else:
                if startup.is_visible:
                    is_public[startup.id] = True
                    industry = startup.primary_industry.parent.name if (
                        startup.primary_industry.parent
                    ) else startup.primary_industry.name
                    industry_startup_ids[industry].append(startup.id)
                    already_listed_startups[startup.id] = len(startups)
                    startups.append({
                        'name': startup.name,
                        'is_visible': startup.is_visible,
                        'profile_url': profile_urls[startup.id],
                        'logo_url': (startup.high_resolution_logo.url if
                                    startup.high_resolution_logo else ''),
                        'image_token': self.get_image_token(
                            startup.high_resolution_logo.name) if (
                            startup.high_resolution_logo) else '',
                        'statuses': [
                            self.status_dict(startup_status),
                        ] if self.status_displayable(startup_status) else [],
                    })
                    if startups[-1]['statuses']:
                        self.status_groups[(
                            startup_status.startup_id,
                            startup_status.program_startup_status.status_group)
                        ] = startup_status.program_startup_status.startup_status
                else:
                    is_public[startup.id] = False
                    pstatus = startup_status.program_startup_status
                    if pstatus.include_stealth_startup_names:
                        stealth_still_listed[startup.id] = True
                        industry = startup.primary_industry.parent.name if (
                            startup.primary_industry.parent
                        ) else startup.primary_industry.name
                        industry_startup_ids[industry].append(startup.id)
                        already_listed_startups[startup.id] = len(startups)
                        startups.append({
                            'name': startup.name,
                            'is_visible': False,
                            'profile_url': '',
                            'logo_url': '',
                            'image_token': '',
                            'statuses': [],
                        })
                    else:
                        stealth_still_listed[startup.id] = False
        pfilter = {
            'program_startup_status__badge_display__in': self.acceptable_badge_display
        }
        for leftover_startup_status in StartupStatus.objects.filter(
                startup_id__in=list(already_listed_startups.keys())
        ).filter(**pfilter).exclude(
            program_startup_status__status_group__in=self.status_groups
        ).exclude(id__in=[ss.id for ss in query.all()]).select_related(
            'program_startup_status',
        ).all():
            startups[already_listed_startups[leftover_startup_status.startup.id]][
                'statuses'].append(self.status_dict(leftover_startup_status))

        if 'group_by' in list(request.GET):
            key = request.GET.get('group_by').lower()
            if key == 'industry':
                data["groups"] = [{
                    'group_title': industry_name,
                    'startups': [
                        startups[
                            already_listed_startups[startup_id]
                        ] for startup_id in ids]} for
                    industry_name, ids in list(industry_startup_ids.items())]
            elif key.startswith('statusgroup:'):
                groupname = key.split(':')[1]
                groups = {}
                for (startup_id, status_group), status in self.status_groups.items():
                    if status_group == groupname:
                        startup = startups[already_listed_startups[startup_id]]
                        if status in groups:
                            groups[status].append(startup)
                        else:
                            groups[status] = [startup, ]
                data['groups'] = [{'group_title': k, 'startups': v}
                                for k, v in list(groups.items())]
            else:
                raise Exception(
                    "GroupBy param {0} not valid".format(
                        request.POST.get('GroupBy')))
            if request.POST.get('IncludeAllGroup', 'Y') != 'N':
                data["groups"] = [{
                    'group_title': 'All',
                    'startups': startups}, ] + data["groups"]
        else:
            data["startups"] = startups
        return HttpResponse(json.dumps(data), content_type="application/json")