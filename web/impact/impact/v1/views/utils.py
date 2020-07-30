# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from pytz import timezone

from accelerator.models import ACTIVE_PROGRAM_STATUS
from mc.utils import swapper_model
UserRole = swapper_model("UserRole")


HOUR_MINUTE_FORMAT = "%I:%M %p"
MONTH_DAY_FORMAT = "%B %d"
DEFAULT_TIMEZONE = "UTC"


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


def email_template_path(template_name):
    return "emails/{}".format(template_name)


# Note: this function should be replaced with calls to
# office_hour.local_start once the re-monolith is complete
def localized_office_hour_start_time(office_hour):
    tz = timezone(get_timezone(office_hour))
    return office_hour.start_date_time.astimezone(tz)


# Note: this function should be replaced with calls to
# office_hour.local_end once the re-monolith is complete
def localized_office_hour_end_time(office_hour):
    tz = timezone(get_timezone(office_hour))
    return office_hour.end_date_time.astimezone(tz)


def is_office_hour_reserver(user):
    """Returns True iff user has an office-hour reserver user role
    with respect to an active program
    Office-hour reserver roles are FINALIST, AIR, ALUM
    """
    reserver_roles = [UserRole.FINALIST, UserRole.AIR, UserRole.ALUM]
    return user.programrolegrant_set.filter(
        program_role__user_role__name__in=reserver_roles,
        program_role__program__program_status=ACTIVE_PROGRAM_STATUS).exists()


def office_hour_time_info(office_hour, last_office_hour=None):
    start_time = localized_office_hour_start_time(office_hour)
    last_office_hour = last_office_hour or office_hour
    end_time = localized_office_hour_end_time(last_office_hour)
    return {"start_time": start_time.strftime(HOUR_MINUTE_FORMAT),
            "end_time": end_time.strftime(HOUR_MINUTE_FORMAT),
            "date": start_time.strftime(MONTH_DAY_FORMAT),
            "timezone": get_timezone(office_hour)}


def get_timezone(office_hour):
    if office_hour.location and office_hour.location.timezone:
        return office_hour.location.timezone
    return DEFAULT_TIMEZONE
