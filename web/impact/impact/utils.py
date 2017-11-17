# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
import dateutil.parser
from pytz import utc

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Q
from django.utils.formats import get_format


DAWN_OF_TIME = utc.localize(datetime.strptime(
    "2010-01-01T00:00:00Z",
    "%Y-%m-%dT%H:%M:%SZ"))  # format based on browsable API output

UPDATE_STATEMENT = "UPDATE {table} SET updated_at = %s WHERE id = %s"


def override_updated_at(model, value):
    # Yes, this big of stick is needed to change the update_at field
    with connection.cursor() as cursor:
        sql = UPDATE_STATEMENT.format(table=model._meta.db_table)
        cursor.execute(sql, [value, model.id])


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


def model_name_case(view, model):
    related_model = view.kwargs.get('related_model')
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
