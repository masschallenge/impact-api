# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.utils.safestring import mark_safe
from embed_video.backends import (
    detect_backend,
    UnknownBackendException,
    UnknownIdException
)
from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V0APIPermissions,
)
from accelerator.models import ProgramStartupStatus
from impact.utils import get_profile
from impact.v0.api_data.startup_detail_data import StartupDetailData
from impact.v0.views.base_media_info import BaseMediaInfo
from impact.v0.views.utils import (
    BADGE_DISPLAYS,
    encrypt_image_token,
    logo_url,
    status_description,
)


DEFAULT_PROFILE_BACKGROUND_COLOR = "217181"
DEFAULT_PROFILE_TEXT_COLOR = "FFFFFF"
EMPTY_DETAIL_RESULT = {
    "additional_industries": [],
    "facebook_url": "",
    "full_elevator_pitch": "",
    "image_token": "",
    "is_visible": False,
    "linked_in_url": "",
    "logo_url": "",
    "name": None,
    "primary_industry": "",
    "profile_background_color": "",
    "profile_text_color": "",
    "public_inquiry_email": "",
    "short_pitch": "",
    "statuses": [],
    "team_members": [],
    "twitter_handle": "",
    "video_elevator_pitch_url": "",
    "website_url": "",
}
MAX_VIDEO_WIDTH = 960
MAX_VIDEO_HEIGHT = 720


class StartupDetailView(APIView):
    permission_classes = (
        V0APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request):
        self.data = StartupDetailData(request.data)
        if self.data.valid():
            return Response(self._calc_result())
        return Response(status=404, data=self.data.errors)

    def _calc_result(self):
        startup = self.data.startup
        if not startup.is_visible:
            return EMPTY_DETAIL_RESULT
        return {
            "additional_industries": [
                industry.name for industry in
                startup.additional_industries.all()],
            "facebook_url": startup.facebook_url,
            "full_elevator_pitch": startup.full_elevator_pitch,
            "is_visible": startup.is_visible,
            "linked_in_url": startup.linked_in_url,
            "name": startup.name,
            "primary_industry": startup.primary_industry.name,
            "public_inquiry_email": startup.public_inquiry_email,
            "short_pitch": startup.short_pitch,
            "twitter_handle": startup.twitter_handle,
            "website_url": startup.website_url,

            "image_token": encrypt_image_token(startup.high_resolution_logo),
            "logo_url": logo_url(startup),
            "profile_background_color":
                "#" + (startup.profile_background_color or
                       DEFAULT_PROFILE_BACKGROUND_COLOR),
            "profile_text_color": "#" + (startup.profile_text_color or
                                         DEFAULT_PROFILE_TEXT_COLOR),
            "statuses": _statuses(startup, self.data.program),
            "team_members": self._team_members(),
            "video_elevator_pitch_url":
                _video_link(startup.video_elevator_pitch_url),
        }

    def _team_members(self):
        base_url = BaseMediaInfo.url()
        return [_user_description(member, base_url)
                for member in _find_members(self.data.startup)]


def _statuses(startup, program):
    statuses = ProgramStartupStatus.objects.filter(
        startup_list_include=True,
        startupstatus__startup=startup,
        badge_display__in=BADGE_DISPLAYS)
    if program:
        statuses = statuses.filter(program=program)
    return [status_description(status.startup_status)
            for status in statuses]


def _user_description(member, base_url):
    user = member.user
    result = {
        "first_name": user.last_name,
        "last_name": user.first_name,
        "email": user.email,
        "title": member.title,
    }
    result.update(_image_fields(user, base_url))
    return result


def _image_fields(user, base_url):
    profile = get_profile(user)
    image = profile.image if profile else None
    return {
        "photo_url": base_url + str(image) if image else "",
        "photo_token": encrypt_image_token(image) if image else "",
    }


def _find_members(startup):
    return startup.startupteammember_set.filter(
        display_on_public_profile=True
    ).order_by("user__first_name", "user__last_name")


def _video_link(video_url):
    try:
        backend = detect_backend(video_url)
        return mark_safe(backend.get_embed_code(MAX_VIDEO_HEIGHT,
                                                MAX_VIDEO_WIDTH))
    except UnknownBackendException:
        return ""
    except UnknownIdException:
        return ""
