# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings

from mc.models import (
    Site,
    SiteProgramAuthorization,
)

PADDING_CHAR = '='

BADGE_DISPLAYS = ("STARTUP_LIST", "STARTUP_LIST_AND_PROFILE")


def logo_url(startup):
    """
    Use the stored filename to generate a ServerlessImageHandler URL
    """
    logo_field = startup.high_resolution_logo
    if not logo_field:
        return ""
    else:
        template = settings.IMAGE_RESIZE_HOST + settings.IMAGE_RESIZE_TEMPLATE
        return template.format(logo_field.name)


def status_description(status):
    return {
        "status_badge_token": "",  # Not used as far as I can tell
        "status_badge_url": "",  # Not used as far as I can tell
        "status_name": status,
    }


def base_program_url(program):
    site = Site.objects.first()
    base_url = ""
    for spa in SiteProgramAuthorization.objects.filter(
            site=site, program=program):
        if spa.startup_profile_base_url:
            base_url = spa.startup_profile_base_url
            break
    return pad_slash(base_url)


def pad_slash(url):
    if url and url[-1] != "/":
        return url + "/"
    return url
