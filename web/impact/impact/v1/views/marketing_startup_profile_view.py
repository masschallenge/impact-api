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
from django.utils.safestring import mark_safe
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
from embed_video.backends import (
    UnknownBackendException,
    UnknownIdException,
    VideoDoesntExistException,
    detect_backend,
)
from impact.v1.views.impact_view import ImpactView
from impact.v1.views.utils import (
    pad,
    normalize_url_scheme,
)

logger = logging.getLogger('django.request')
DEFAULT_PROFILE_BACKGROUND_COLOR = "217181"  # default dark blue
DEFAULT_PROFILE_TEXT_COLOR = "FFFFFF"
VIDEO_LINK_EMBED_MSG = "{} on URL: {}"


class MarketingStartupProfileView(ImpactView):
    view_name = "marketing_startup_profile_view"

    def __init__(self):
        self.acceptable_badge_display = (
            BADGE_STARTUP_PROFILE, BADGE_STARTUP_LIST_AND_PROFILE)
        self.status_groups = set()
    
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

    def website(self, website_url):
        return normalize_url_scheme(website_url)

    def video_link_embed(self, url):
        """return an iframe-style embed for the provided video link"""
        try:
            backend = detect_backend(url)
            return mark_safe(backend.get_embed_code(960, 720))
        except (UnknownBackendException,
                UnknownIdException,
                VideoDoesntExistException,
                ConnectionError) as e:
            logger.warning(VIDEO_LINK_EMBED_MSG.format(str(e), url))
            return ""

    def get(self, request):
        program_names = request.GET.getlist('program_key')
        site_name = request.GET['site_name']
        if not request.GET['startup_key']:
            raise ValueError("No startup given.")
        name = None
        try:
            # contains non-integers
            if re.match(r".*\D.*", request.GET['startup_key']):
                startup = Startup.objects.select_related('primary_industry').get(
                    organization__url_slug=request.GET['startup_key'])
            else:
                startup = Startup.objects.select_related(
                    'primary_industry').get(pk=request.GET['startup_key'])
        except ObjectDoesNotExist:
            raise PermissionDenied
        is_public = startup.is_visible
        data = {}

        if is_public:
            addition_industry_categories = startup.additional_industries
            data = {
                "name": startup.name,
                "is_visible": startup.is_visible,
                "logo_url": (
                    startup.high_resolution_logo.url
                ) if startup.high_resolution_logo else "",
                "image_token": getImageToken(
                    startup.high_resolution_logo.name
                ) if startup.high_resolution_logo else "",
                "primary_industry": startup.primary_industry.name,
                "additional_industries": [
                    industry.name for industry in
                    addition_industry_categories.all()
                ], "short_pitch": startup.short_pitch,
                "full_elevator_pitch": startup.full_elevator_pitch,
                "website_url": self.website(
                    startup.website_url),
                "twitter_handle": startup.twitter_handle,
                "public_inquiry_email": startup.public_inquiry_email,
                "facebook_url": startup.facebook_url,
                "linked_in_url": startup.linked_in_url,
                "video_elevator_pitch_url": self.video_link_embed(
                    startup.video_elevator_pitch_url),
                "statuses": [],
                "team_members": [],
                "profile_background_color": "#" + (
                    startup.profile_background_color or
                    DEFAULT_PROFILE_BACKGROUND_COLOR),
                # format "#FFFFFF"
                # format "#FFFFFF"
                "profile_text_color": "#" + (
                    startup.profile_text_color or
                    DEFAULT_PROFILE_TEXT_COLOR)
            }
            print(">>>>>>>", data, startup, "\n\n >>>>", type(startup))
            statuses = StartupStatus.objects.order_by(
                'program_startup_status__sort_order',
                'program_startup_status__startup_status'). \
                select_related('program_startup_status').filter(startup=startup)
            if request.POST.get('ProgramKey'):
                statuses.filter(
                    program_startup_status__program__name=request.POST.get(
                        'ProgramKey')
                )
            for startup_status in statuses:
                if self.status_displayable(startup_status):
                    data['statuses'].append(self.status_dict(startup_status))
                    self.status_groups.add(
                        (startup_status.startup_id,
                        startup_status.program_startup_status.status_group))

            # If this site has access to team members for a program which the
            # startup belongs to, fill them in
            # 
            # if Site.is_allowed(
            #         request.POST.get('SiteName'),
            #         request.POST.get('SecurityKey'),
            #         'startup_team_members',
            #         startup=request.POST.get('StartupKey')):
            team_members = StartupTeamMember.objects.filter(
                startup=startup).order_by(
                    'user__last_name', 'user__first_name')
            team = []
            for member in team_members:
                if member.display_on_public_profile:
                    team.append({
                        'first_name': member.user.first_name,
                        'last_name': member.user.last_name,
                        'email': member.user.email,
                        'title': member.title,
                        'photo_url': (
                            member.user.get_profile().image.url
                        ) if (
                            member.user.get_profile().image
                        ) else '',
                        'photo_token': self.get_image_token(
                            member.user.get_profile().image.name
                        ) if member.user.get_profile().image else '',
                    })
            data.update({'team_members': team})
        else:
            data = {
                "name": name,
                "is_visible": False,
                "logo_url": "",
                "image_token": "",
                "primary_industry": "",
                "additional_industries": [],
                "short_pitch": "",
                "full_elevator_pitch": "",
                "website_url": "",
                "twitter_handle": "",
                "public_inquiry_email": "",
                "facebook_url": "",
                "linked_in_url": "",
                "video_elevator_pitch_url": "",
                "statuses": [],
                "team_members": [],
                "profile_background_color": "",
                "profile_text_color": "",
            }
        return HttpResponse(json.dumps(data), content_type="application/json")