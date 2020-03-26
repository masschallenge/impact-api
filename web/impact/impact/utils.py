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


def get_user_program_and_startup_roles(user,
                                       user_roles_of_interest=[],
                                       startup_roles_of_interest=[]):
    """
    Fetch program roles for the user and startup roles for
    any startups the user belongs to
    NOTE: the name is deceptive
    """

    user_prg_roles = _get_user_prg_role_by_program_family(
        user, user_roles_of_interest)
    startup_prg_roles = _get_user_startup_prg_role_by_program_family(
        user, startup_roles_of_interest
    )
    return _clean_role_names(_combine_prg_roles(
        user_prg_roles=user_prg_roles,
        startup_prg_roles=startup_prg_roles
    ))


def _clean_role_names(role_names):
    return [_clean_role_name(role_name) for role_name in role_names]


def _clean_role_name(role_name):
    "Convert to title case and remove parenthesised program abbreviations"
    role_name = role_name.title().split(" (")[0]


def _get_user_prg_role_by_program_family(user, user_roles=[]):
    """
    Return a user's program role grants grouped by the program family
    Filter role grants by the provided user role or return
    all program role grants the user has ever had
    """

    query = user.programrolegrant_set.filter(
        program_role__user_role__isnull=False
    )
    if user_roles:
        query = query.filter(
            program_role__user_role__name__in=user_roles)
    result = query.values_list(
        'program_role__name',
        'program_role__program__program_family__name')
    return _group_by_program_family(result)


def _get_user_startup_prg_role_by_program_family(user,
                                                 startup_roles=[]):
    """
    Fetch the program status for all startups a given user belongs to
    """

    startups = user.startup_set.all()

    result = []
    for startup in startups:
        query = startup.program_startup_statuses()
        if startup_roles:
            query = query.filter(
                startup_role__name__in=startup_roles
            )
        result = query.values_list("startup_status",
                                   "program__program_family__name")

    return _group_by_program_family(result)


def _group_by_program_family(array):
    by_program_family = {}
    for program_role, program_family in array:
        if by_program_family.get(program_family):
            by_program_family[program_family].append(program_role)
        else:
            by_program_family[program_family] = [program_role]
    return by_program_family


def _combine_prg_roles(user_prg_roles, startup_prg_roles):
    """
    Collapse two dictionaries with list values into one by merging
    lists having the same key
    """

    for key, value in startup_prg_roles.items():
        if user_prg_roles.get(key):
            user_prg_roles[key] = user_prg_roles[key] + value
        else:
            user_prg_roles[key] = value

    return user_prg_roles
