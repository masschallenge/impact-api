# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import re
from django.core.exceptions import ValidationError
from django.core.validators import (
    URLValidator,
    validate_email,
)
from impact.models.base_profile import (
    PHONE_MAX_LENGTH,
    TWITTER_HANDLE_MAX_LENGTH,
)


def merge_fields(field, extension):
    if not isinstance(field, dict) or not isinstance(extension, dict):
        return field
    result = {}
    for key, value in field.items():
        result[key] = merge_fields(value, extension.get(key))
    for key in set(extension.keys()) - set(field.keys()):
        result[key] = extension[key]
    return result


PK_FIELD = {
    "json-schema": {
        "type": "integer",
        "readOnly": True,
    },
    "PATCH": {"required": True},
}

BOOLEAN_FIELD = {
    "json-schema": {
        "type": "boolean",
    },
    "PATCH": {"required": False},
    "POST": {"required": False},
    "default": False,
}

INTEGER_ARRAY_FIELD = {
    "json-schema": {
        "type": "array",
        "item": {
            "type": "integer"
        },
    },
}

INTEGER_FIELD = {
    "json-schema": {
        "type": "integer"
    },
}

FLOAT_FIELD = {
    "json-schema": {
        "type": "number"
    },
}

READ_ONLY_ID_FIELD = {
    "json-schema": {
        "type": "integer",
        "readOnly": True,
    },
}

READ_ONLY_STRING_FIELD = {
    "json-schema": {
        "type": "string",
        "readOnly": True,
    },
}

POST_REQUIRED = {"POST": {"required": True}}

STRING_FIELD = {
    "json-schema": {
        "type": "string",
    },
    "PATCH": {"required": False},
    "POST": {"required": False},
}
REQUIRED_STRING_FIELD = merge_fields(POST_REQUIRED, STRING_FIELD)

EMAIL_FIELD = {
    "json-schema": {
        "type": "string",
        "description": "Must be valid email per the Django EmailValidator",
    },
    "PATCH": {"required": False},
    "POST": {"required": False},
}
REQUIRED_EMAIL_FIELD = merge_fields(POST_REQUIRED, EMAIL_FIELD)

PHONE_PATTERN = '^[0-9x.+() -]{{0,{}}}$'.format(PHONE_MAX_LENGTH)
PHONE_REGEX = re.compile(PHONE_PATTERN)
PHONE_FIELD = {
    "json-schema": {
        "type": "string",
        "pattern": PHONE_PATTERN,
    },
    "PATCH": {"required": False},
    "POST": {"required": False},
}

URL_FIELD = merge_fields(
    STRING_FIELD,
    {
        "json-schema": {
            "description": "Must be valid URL per the Django URLValidator",
         },
    })

URL_SLUG_FIELD = merge_fields(STRING_FIELD,
                              {"json-schema": {"pattern": "^[a-zA-Z0-9_-]+$"}})

TWITTER_PATTERN = '^\S{{0,{}}}$'.format(TWITTER_HANDLE_MAX_LENGTH)
TWITTER_REGEX = re.compile(TWITTER_PATTERN)
TWITTER_FIELD = merge_fields(STRING_FIELD,
                             {"json-schema": {"pattern": TWITTER_PATTERN}})


INVALID_BOOLEAN_ERROR = ("Invalid {field}: "
                         "Expected 'true' or 'false' not {value}")
INVALID_CHOICE_ERROR = ("Invalid {field}: "
                        "Expected {choices} not {value}")
INVALID_EMAIL_ERROR = ("Invalid {field}: "
                       "Expected '{value}' to be valid email address")
INVALID_REGEX_ERROR = "Invalid {field}: Expected '{value}' to match '{regex}'"
INVALID_STRING_ERROR = "Invalid {field}: Expected a String not {value}"
INVALID_URL_ERROR = "Invalid {field}: Expected '{value}' to be a valid URL"
MISSING_SUBJECT_ERROR = "Database error: missing object"


class ModelHelper(object):
    VALIDATORS = {}

    def __init__(self, subject):
        self.subject = subject
        self.errors = []
        if not self.subject:
            self.errors.append(MISSING_SUBJECT_ERROR)

    def serialize(self, fields):
        result = {}
        for field in fields:
            value = self.field_value(field)
            if value is not None:
                result[field] = value
        return result

    def field_value(self, field):
        result = getattr(self, field, None)
        if result is not None:
            return result
        return getattr(self.subject, field, None)

    def field_setter(self, field, value):
        subject = self.subject
        # The following lines would allow a helper to
        # override the subject's setter.  We haven't
        # needed this yet, so leaving this mechanism
        # commented out.
        # attr = getattr(self.__class__, field, None)
        # if attr and attr.fset:
        #     subject = self
        if subject:
            setattr(subject, field, value)

    def validate(self, field, value):
        validator = self.VALIDATORS.get(field)
        if validator:
            value = validator(self, field, value)
        return value

    def save(self):
        if self.subject:
            self.subject.save()

    @classmethod
    def all_objects(cls):
        return cls.model.objects.all()

    def field_name(self, field):
        obj = getattr(self.subject, field, None)
        if hasattr(obj, "name"):
            return obj.name


def validate_boolean(helper, field, value):
    result = value
    if isinstance(result, str):
        result = result.lower()
        if result == 'true':
            result = True
        elif result == 'false':
            result = False
    if not isinstance(result, bool):
        helper.errors.append(INVALID_BOOLEAN_ERROR.format(field=field,
                                                          value=value))
    return result


def validate_string(helper, field, value):
    if not isinstance(value, str):
        helper.errors.append(INVALID_STRING_ERROR.format(field=field,
                                                         value=value))
    return value


def validate_choices(helper, field, value, choices):
    validate_string(helper, field, value)
    if value not in choices:
        helper.errors.append(INVALID_CHOICE_ERROR.format(
                field=field, value=value, choices=format_choices(choices)))
    return value


def format_choices(choices):
    choice_list = list(choices)
    if choice_list:
        result = "', '".join(choice_list[:-1])
        if result:
            result += "' or '"
        result += "%s'" % choice_list[-1]
        return "'" + result


def validate_regex(helper, field, value, regex):
    if not regex.match(value):
        helper.errors.append(INVALID_REGEX_ERROR.format(field=field,
                                                        value=value,
                                                        regex=regex.pattern))
    return value


def validate_email_address(helper, field, value):
    try:
        validate_email(value)
    except ValidationError:
        helper.errors.append(INVALID_EMAIL_ERROR.format(field=field,
                                                        value=value))
    return value


def validate_url(helper, field, value):
    if value:
        try:
            URLValidator(schemes=["http", "https"])(value)
        except ValidationError:
            helper.errors.append(INVALID_URL_ERROR.format(field=field,
                                                          value=value))
    return value


def json_object(properties):
    return {
        "type": "object",
        "properties": properties,
    }


def json_array(item):
    return {
        "type": "array",
        "item": item,
    }


def json_list_wrapper(item):
    return json_object({
            "count": INTEGER_FIELD,
            "next": URL_FIELD,
            "previous": URL_FIELD,
            "results": json_array(item)})


def json_simple_list(item, list_key):
    return json_object({list_key: json_array(item)})
