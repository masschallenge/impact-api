# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import os
import re
from time import time

import base64
import hashlib
from Crypto.Cipher import AES

from django.conf import settings

from impact.models import (
    Site,
    SiteProgramAuthorization,
)
from impact.v0.views.base_media_info import BaseMediaInfo


BADGE_DISPLAYS = ("STARTUP_LIST", "STARTUP_LIST_AND_PROFILE")
IMAGE_TOKEN_BLOCK_SIZE = 16


def encrypt_image_token(token, password=None):
    if token:
        if password is None:
            password = settings.V0_IMAGE_PASSWORD
        iv = os.urandom(IMAGE_TOKEN_BLOCK_SIZE)
        key = hashlib.sha256(password).hexdigest()[:32]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        raw = _pad(token + ":" + str(time()))
        return base64.urlsafe_b64encode((iv + cipher.encrypt(raw)))
    return b""


def _pad(text):
    encoded_bytes = text.encode("utf-8")
    length = len(encoded_bytes)
    pad_size = IMAGE_TOKEN_BLOCK_SIZE - length % IMAGE_TOKEN_BLOCK_SIZE
    padding = pad_size * chr(pad_size)
    return encoded_bytes + padding.encode("utf-8")


def logo_url(startup):
    if not startup.high_resolution_logo:
        return ""
    schema = "^(http|https)://"
    if re.match(schema, startup.high_resolution_logo, re.IGNORECASE):
        return startup.high_resolution_logo
    return BaseMediaInfo.url(startup.high_resolution_logo)


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
