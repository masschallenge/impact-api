# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from datetime import datetime
from pytz import utc
from impact.models import BaseProfile
from django.db.models import Q
from django.utils.formats import get_format
import dateutil.parser


DAWN_OF_TIME = utc.localize(datetime.strptime(
        "2010-01-01T00:00:00Z",
        "%Y-%m-%dT%H:%M:%SZ"))  # format based on browsable API output


def parse_date(date_str):
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return dateutil.parser(date_str, item)
        except (ValueError, TypeError):
            continue
    if date_str:
        return dateutil.parser.parse(date_str)


def get_profile(user):
    try:
        user_type = user.baseprofile.user_type
        if user_type == "ENTREPRENEUR":
            return user.entrepreneurprofile
        if user_type == "EXPERT":
            return user.expertprofile
        return user.memberprofile
    except BaseProfile.DoesNotExist:
        return None


def compose_filter(key_pieces, value):
    return {"__".join(key_pieces): value}


def next_instance(instance, query):
    return _find_instance(instance, Q(id__gt=instance.id) & query, "id")


def previous_instance(instance, query):
    return _find_instance(instance, Q(id__lt=instance.id) & query, "-id")


def _find_instance(instance, query, order):
    return type(instance).objects.filter(query).order_by(order).first()
