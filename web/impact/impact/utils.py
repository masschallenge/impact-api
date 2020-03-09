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


"""
fetch a program role assigned to an user and those assigned to the startups
the user belong to

Time, Space, Query Complexity
Query: amount to the query complexity of the two helper function that
access the DB (see functions for query comp analysis for each)

Time/Space amount to time and space complexity of the three helper functions
(see functions for time/space comp analysis for each)
    """
def get_user_program_roles(
    user, user_roles_of_interest=[], startup_roles_of_interest=[]):

        user_prg_roles = _get_user_prg_role_by_program_family(
            user, user_roles_of_interest)
        startup_prg_roles = _get_user_startup_prg_role_by_program_family(
           user, startup_roles_of_interest
        )
        return _combine_prg_roles(
            user_prg_roles=user_prg_roles, startup_prg_roles=startup_prg_roles
        )

"""
return a use's program role grants grouped by the program family
filter role grants by the provided user role or return
all program role grant the user has ever had

Time, Space Complexity
O(n): time and space where n is the number of item in the result list
"""
def _get_user_prg_role_by_program_family(user, user_roles=[]):
    query = user.programrolegrant_set.filter(
        program_role__user_role__isnull=False
    )
    if user_roles:
        query = query.filter(
            program_role__user_role__name__in=user_roles)
    result = query.values_list(
        'program_role__name', 'program_role__program__program_family__name')
    prg_group = {}
    for program_role_grant, program_family in result:
        if prg_group.get(program_family):
            prg_group[program_family].append(program_role_grant)
        else:
            prg_group[program_family] = [program_role_grant]
    return prg_group

"""
fetch a the program status for all startup a given user
belongs to

Time, Space, Query Complexity
Query: 0(n + 1) where n is the number of startup a user belongs to
since for every startup in that list we are fetching the program status.
and the +1 is for the query to fetch all startup for the user

O(nm)Time/Space where n is the number of startup and m is
the number of program_startup_status
"""
def _get_user_startup_prg_role_by_program_family(user, startup_roles=[]):
    startups = user.startup_set.all()
    startup_status_group = {}
    for startup in startups:
        query = startup.program_startup_statuses()
        if startup_roles:
            query = query.filter(
                startup_role__name__in=startup_roles
            )
        result = query.values_list("startup_status", "program__program_family__name")
        for startup_status, program_family in result:
            if startup_status_group.get(program_family):
                startup_status_group[program_family].append(startup_status)
            else:
                startup_status_group[program_family] = [startup_status]

    return startup_status_group

"""
collapse two dictory with list values into one where similar keys values
in both dictionaries are merged

Time, Space Complexity
O(n)Time/Space; where n is the number of items in the startup_prg_roles

"""
def _combine_prg_roles(user_prg_roles, startup_prg_roles):
    for key, value in startup_prg_roles.items():
        if user_prg_roles.get(key):
            user_prg_roles[key] = user_prg_roles[key] + value
        else:
            user_prg_roles[key] = value

    return user_prg_roles
