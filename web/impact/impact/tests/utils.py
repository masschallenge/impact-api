# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from pytz import utc
from datetime import (
    datetime,
    timedelta,
)


def days_from_now(days):
    return utc.localize(datetime.now() + timedelta(days))


def months_from_now(months):
    return days_from_now(months * 30)


def match_errors(data, errors):
    for key, value in data.items():
        found = False
        for error in errors:
            if key in error and value in error:
                found = True
        if not found:
            return False
    return True


def find_events(history, event_type):
    return [event for event in history
            if event["event_type"] == event_type]
