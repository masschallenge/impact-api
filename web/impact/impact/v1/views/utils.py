# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from future import standard_library
from django.conf import settings
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