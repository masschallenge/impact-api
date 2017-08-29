# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from datetime import datetime
from pytz import utc
from impact.models import BaseProfile
from django.utils.formats import get_format
import dateutil.parser
REQUIRED_USER_KEYS = [
    "email",
    "first_name",
    "last_name",
]
OPTIONAL_USER_KEYS = [
    "is_active",
]
USER_KEYS = REQUIRED_USER_KEYS + OPTIONAL_USER_KEYS
REQUIRED_PROFILE_KEYS = [
    "gender",
]
PROFILE_KEYS = REQUIRED_PROFILE_KEYS
ALL_USER_RELATED_KEYS = USER_KEYS + PROFILE_KEYS
KEY_TRANSLATIONS = {
    "first_name": "full_name",
    "last_name": "short_name",  # Yes, this is correct
}
VALID_GENDERS = ["f", "m", "o", "p"]
INVALID_GENDER_ERROR = ("Invalid gender: '{}'. Valid values are "
                        "'f' or 'female', 'm' or 'male', "
                        "'o' or 'other', and 'p' or 'prefer not to state'")
GENDER_TRANSLATIONS = {
    "female": "f",
    "male": "m",
    "other": "o",
    "prefer not to state": "p",
}
DAWN_OF_TIME = utc.localize(datetime.strptime(
        "2010-01-01T00:00:00Z",
        "%Y-%m-%dT%H:%M:%SZ"))  # format based on what the browsable API shows


def parse_date(date_str):
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return dateutil.parser(date_str, item)
        except (ValueError, TypeError):
            continue
    if date_str:
        return dateutil.parser.parse(date_str)


def compose_filter(key_pieces, value):
    return {"__".join(key_pieces): value}


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


def user_gender(user):
    profile = get_profile(user)
    if profile:
        return profile.gender
    return None


def find_gender(gender):
    if not hasattr(gender, "lower"):
        return None
    gender = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    if gender in VALID_GENDERS:
        return gender
    return None
