# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from pytz import timezone
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
    tz = timezone(office_hour.location.timezone)
    return office_hour.start_date_time.astimezone(tz)
    
