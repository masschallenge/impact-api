# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
import base64
import hashlib
import os

from Cryptodome.Cipher import AES
from future import standard_library
from django.conf import settings
from time import time
from urllib.parse import urlsplit

standard_library.install_aliases()
PADDING_CHAR = '='
VALID_KEYS_NOTE = "Valid keys are: {}"


def valid_keys_note(keys):
    return VALID_KEYS_NOTE.format(", ".join(sorted(keys)))


def coalesce_dictionaries(data, merge_field="id"):
    """Takes a sequence of dictionaries, merges those that share the
    same merge_field, and returns a list of resulting dictionaries"""
    result = {}
    for datum in data:
        merge_id = datum[merge_field]
        item = result.get(merge_id, {})
        item.update(datum)
        result[merge_id] = item
    return result.values()


def map_data(klass, query, order, data_keys, output_keys):
    result = klass.objects.filter(query).order_by(order)
    data = result.values_list(*data_keys)
    return [dict(zip(output_keys, values))
            for values in data]

def pad(unpadded_str):
    remainder = len(unpadded_str) % settings.IMAGE_TOKEN_BLOCK_SIZE
    pad_size = settings.IMAGE_TOKEN_BLOCK_SIZE - remainder
    padding = pad_size * PADDING_CHAR
    return unpadded_str + padding


def unpad(padded_string):
    padding_char = padded_string[-1]
    first_index_of_pad = padded_string.find(padding_char)
    return padded_string[:first_index_of_pad]

def normalize_url_scheme(url):
    if not url:
        return ''
    if not urlsplit(url).scheme:
        return "http://" + url
    return url

def get_image_token(name):
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

def status_dict(startup_status):
    return {
        'status_name': startup_status.program_startup_status.startup_status,
        'status_badge_url': (
            startup_status.program_startup_status.badge_image.url
        )
        if startup_status.program_startup_status.badge_image else '',
        'status_badge_token': get_image_token(
            startup_status.program_startup_status.badge_image.name
        ) if startup_status.program_startup_status.badge_image else '',
    }

def status_displayable(startup_status, status_groups, acceptable_badge_display):
    pstatus = startup_status.program_startup_status
    return (
        not startup_status.program_startup_status.status_group or (
            startup_status.startup_id,
            startup_status.program_startup_status.status_group
        ) not in status_groups
    ) and (pstatus.badge_display in acceptable_badge_display)