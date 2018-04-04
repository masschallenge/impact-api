# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import base64
import hashlib
import os
from time import time

from Crypto.Cipher import AES
from django.conf import settings

from accelerator.models import (
    Site,
    SiteProgramAuthorization,
)

PADDING_CHAR = '='

BADGE_DISPLAYS = ("STARTUP_LIST", "STARTUP_LIST_AND_PROFILE")
IMAGE_TOKEN_BLOCK_SIZE = 16


def encrypt_image_token(token, password=None):
    if token:
        if password is None:
            password = settings.V0_IMAGE_PASSWORD
        iv = os.urandom(IMAGE_TOKEN_BLOCK_SIZE)
        key = hashlib.sha256(password).hexdigest()[:32]
        aes = AES.new(key, AES.MODE_CBC, iv)
        time_block = str(time())
        raw = _pad(str(token) + ":" + time_block)
        encrypted = aes.encrypt(raw)
        encoded = base64.urlsafe_b64encode((iv + encrypted))
        return encoded
    return b""


def _pad(text):
    encoded_bytes = text.encode("utf-8")
    length = len(encoded_bytes)
    leftover_size = length % IMAGE_TOKEN_BLOCK_SIZE
    pad_size = IMAGE_TOKEN_BLOCK_SIZE - leftover_size
    padding = pad_size * PADDING_CHAR
    return encoded_bytes + padding.encode("utf-8")


def logo_url(startup):
    if not startup.high_resolution_logo:
        return ""
    return startup.high_resolution_logo.url


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
