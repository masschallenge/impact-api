# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from pytz import timezone
from urllib.parse import urlencode
from urllib.parse import urlunparse
from add2cal import Add2Cal

from accelerator.models import (
    ACTIVE_PROGRAM_STATUS,
    UserRole,
)

VALID_KEYS_NOTE = "Valid keys are: {}"
REMINDER_DATE_FORMAT = "%Y%m%dT%H%M%S"


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
    tz = timezone(office_hour.location.timezone)
    return office_hour.start_date_time.astimezone(tz)


def is_office_hour_reserver(user):
    """Returns True iff user has an office-hour reserver user role
    with respect to an active program
    Office-hour reserver roles are FINALIST, AIR, ALUM
    """
    reserver_roles = [UserRole.FINALIST, UserRole.AIR, UserRole.ALUM]
    return user.programrolegrant_set.filter(
        program_role__user_role__name__in=reserver_roles,
        program_role__program__program_status=ACTIVE_PROGRAM_STATUS).exists()

def _get_reminder_params(office_hour, recipient='finalist'):
    start_datetime = office_hour.start_date_time
    end_datetime = office_hour.end_date_time
    tz = office_hour.get_timezone()
    start_date = start_datetime.astimezone(tz).strftime(REMINDER_DATE_FORMAT)
    end_date = end_datetime.astimezone(tz).strftime(REMINDER_DATE_FORMAT)
    topics_block = ""
    info_block = ""

    if recipient == 'mentor':
        title = "Office hour with %s %s" % (
            office_hour.finalist.first_name,
            office_hour.finalist.last_name)
    else:
        title = "Office hour with %s %s" % (
            office_hour.mentor.first_name,
            office_hour.mentor.last_name)

    if office_hour.topics:
        topics_block = "Topics: {topics}".format(
            topics=office_hour.topics)

    if office_hour.meeting_info:
        info_block = "Meeting info: {info}".format(
            info=office_hour.meeting_info)

    description = """
    {description}

    {topics}

    {info}
    """.format(
        description=office_hour.description,
        topics=topics_block,
        info=info_block)

    return {
        'start': start_date,
        'end': end_date,
        'title': title,
        'description': description,
        'location': office_hour.location_name,
        'timezone': tz
    }


def generate_ical_content(office_hour):
    params = _get_reminder_params(office_hour)
    cal = Add2Cal(**params)
    return cal.ical_content()


def generate_reminder_link(
        office_hour,
        link_type='ical',
        recipient='finalist'):
    params = _get_reminder_params(office_hour, recipient=recipient)
    params['link_type'] = link_type
    host = settings.IMPACT_HOST
    return _build_url(host, params)


def generate_calendar_links(hour, recipient='finalist'):
    return {
        'yahoo_reminder': generate_reminder_link(
            hour,
            link_type='yahoo',
            recipient=recipient),
        'google_reminder': generate_reminder_link(
            hour,
            link_type='google',
            recipient=recipient),
        'ical_reminder': generate_reminder_link(
            hour,
            recipient=recipient),
        'outlook_reminder': generate_reminder_link(
            hour,
            link_type='outlook',
            recipient=recipient),
    }


def _build_url(baseurl, args_dict):

    url_parts = list(urlparse('//' + baseurl + '/api/calendar/reminder/'))
    if args_dict.get('link_type') == 'ical':
        url_parts[0] = 'webcal'
    else:
        url_parts[0] = 'https'
    url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)
