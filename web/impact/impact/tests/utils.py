# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
import sys
from contextlib import contextmanager
from datetime import (
    datetime,
    timedelta,
)
from io import StringIO

from pytz import utc


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


def assert_fields(fields, data):
    for field in fields:
        assert field in data, "%s missing" % field


def assert_fields_missing(fields, data):
    for field in fields:
        assert field not in data, "%s present" % field


def assert_fields_required(fields, data):
    for field in fields:
        error_msg = "Expected %s to be required" % field
        assert "required" in data[field], error_msg


def assert_fields_not_required(fields, data):
    for field in fields:
        error_msg = "Expected %s to not be required" % field
        assert "required" not in data[field], error_msg


def assert_data_is_consistent_with_instance(data, instance):
    for key, val in data.items():
        if val != getattr(instance, key):
            raise AssertionError("%s did not equal %s. (Key: %s)" %
                                 (str(val), str(getattr(instance, key)), key))


@contextmanager
def capture_stderr(command, *args, **kwargs):
    err, sys.stderr = sys.stderr, StringIO()
    try:
        result = command(*args, **kwargs)
        yield result, sys.stderr.read()
    finally:
        sys.stderr = err


def get_ui_notification_dict(success, header, notification):
    return {
        'success': success,
        'header': header,
        'detail': notification
    }
