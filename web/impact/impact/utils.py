# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
import dateutil.parser
from pytz import utc

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.formats import get_format

DAWN_OF_TIME = utc.localize(datetime.strptime(
    "2010-01-01T00:00:00Z",
    "%Y-%m-%dT%H:%M:%SZ"))  # format based on browsable API output


def override_updated_at(instance, timestamp):
    """
    Workaround to set the `updated_at` field of the instance to the given
    `datetime`. Can't use `save()` because that triggers `auto_now`.
    """
    instance_as_qs = instance._meta.default_manager.filter(pk=instance.pk)
    assert instance_as_qs.count() == 1
    instance_as_qs.update(updated_at=timestamp)


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
    except ObjectDoesNotExist:
        return None


def model_name_case(model, related_model):
    if related_model:
        return model + '_' + related_model
    return model


def compose_filter(key_pieces, value):
    return {"__".join(key_pieces): value}


def next_instance(instance, query):
    return _find_instance(instance, Q(id__gt=instance.id) & query, "id")


def previous_instance(instance, query):
    return _find_instance(instance, Q(id__lt=instance.id) & query, "-id")


def _find_instance(instance, query, order):
    return type(instance).objects.filter(query).order_by(order).first()

# return a use's program role grants grouped by the program family
# filter role grants by the provided user role or return
# all program role grant the user has ever had
def get_user_prg_by_programfamily(user, user_roles=[]):
    query = user.programrolegrant_set.filter(
        program_role__user_role__isnull=False
    )
    if user_roles:
        query = query.filter(
            program_role__user_role__name__in=user_roles)
    result = query.values_list(
        'program_role__name', 'program_role__program__program_family__name')
    prg_group = {}
    for prg, pf in result:
        if prg_group.get(pf):
            prg_group[pf].append(prg)
        else:
            prg_group[pf] = [prg]
    return prg_group
