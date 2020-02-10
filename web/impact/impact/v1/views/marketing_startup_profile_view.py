import json
import logging

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
    get_image_token,
    normalize_url_scheme,
    pad,
    status_dict,
    status_displayable,
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
        self.data = {}

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

    def get_public_data(self, startup):
        addition_industry_categories = startup.additional_industries
        self.data = {
            "name": startup.name,
            "is_visible": startup.is_visible,
            "logo_url": (
                startup.high_resolution_logo.url
            ) if startup.high_resolution_logo else "",
            "image_token": get_image_token(
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
            "profile_text_color": "#" + (
                startup.profile_text_color or
                DEFAULT_PROFILE_TEXT_COLOR)
        }

    def get_status(self, startup, program_key):
        statuses = StartupStatus.objects.order_by(
            'program_startup_status__sort_order',
            'program_startup_status__startup_status'). \
            select_related('program_startup_status').filter(startup=startup)
        if program_key:
            statuses.filter(
                program_startup_status__program__name=program_key
            )
        for startup_status in statuses:
            if status_displayable(startup_status,
                self.status_groups, self.acceptable_badge_display):
                self.data['statuses'].append(status_dict(startup_status))
                self.status_groups.add(
                    (startup_status.startup_id,
                    startup_status.program_startup_status.status_group))

    def get_team_members(self, startup):
        # If this site has access to team members for a program which the
        # startup belongs to, fill them in
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
                    'photo_token': get_image_token(
                        member.user.get_profile().image.name
                    ) if member.user.get_profile().image else '',
                })
        self.data.update({'team_members': team})

    def get_non_public_data(self):
        self.data = {
            "name": None,
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

    def get(self, request):
        if not request.GET['startup_key']:
            raise ValueError("No startup given.")
        program_key = request.GET.get('program_key')
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

        if is_public:
            self.get_public_data(startup)
            self.get_status(startup, program_key)
            self.get_team_members(startup)
        else:
            self.get_non_public_data()
        return HttpResponse(json.dumps(self.data), content_type="application/json")