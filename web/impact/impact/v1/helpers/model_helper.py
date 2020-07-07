# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import re

from mc.models import (
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


def json_schema(field_type):
    return {"json-schema": {"type": field_type}}


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

POST_OPTIONAL = {
    "PATCH": {"required": False},
    "POST": {"required": False},
}

POST_REQUIRED = {
    "PATCH": {"required": False},
    "POST": {"required": True},
}

RAW_INTEGER_FIELD = {
    "json-schema": {
        "type": "integer"
    },
}

OPTIONAL_INTEGER_FIELD = merge_fields(POST_OPTIONAL, RAW_INTEGER_FIELD)
REQUIRED_INTEGER_FIELD = merge_fields(POST_REQUIRED, RAW_INTEGER_FIELD)

RAW_FLOAT_FIELD = {
    "json-schema": {
        "type": "number"
    },
}

OPTIONAL_FLOAT_FIELD = merge_fields(POST_OPTIONAL, RAW_FLOAT_FIELD)
REQUIRED_FLOAT_FIELD = merge_fields(POST_REQUIRED, RAW_FLOAT_FIELD)

READ_ONLY_INTEGER_FIELD = {
    "json-schema": {
        "type": "integer",
        "readOnly": True,
    },
}

READ_ONLY_ID_FIELD = READ_ONLY_INTEGER_FIELD

READ_ONLY_OBJECT_FIELD = {
    "json-schema": {
        "type": "object",
        "readOnly": True,
    },
}

RAW_STRING_FIELD = {
    "json-schema": {
        "type": "string",
    },
}

READ_ONLY_STRING_FIELD = {
    "json-schema": {
        "type": "string",
        "readOnly": True,
    },
}

OPTIONAL_STRING_FIELD = merge_fields(POST_OPTIONAL, RAW_STRING_FIELD)
REQUIRED_STRING_FIELD = merge_fields(POST_REQUIRED, RAW_STRING_FIELD)

STRING_ARRAY_FIELD = {
    "json-schema": {
        "type": "array",
        "item": {
            "type": "string"
        },
    },
}

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

RAW_URL_FIELD = merge_fields(
    RAW_STRING_FIELD,
    {
        "json-schema": {
            "description": "Must be valid URL per the Django URLValidator",
        },
    })
OPTIONAL_URL_FIELD = merge_fields(POST_OPTIONAL, RAW_URL_FIELD)

URL_SLUG_FIELD = merge_fields(
    OPTIONAL_STRING_FIELD,
    {
        "json-schema": {"pattern": "^[a-zA-Z0-9_-]+$"},
    })

TWITTER_PATTERN = r'^\S{{0,{}}}$'.format(TWITTER_HANDLE_MAX_LENGTH)
TWITTER_REGEX = re.compile(TWITTER_PATTERN)
TWITTER_FIELD = merge_fields(
    OPTIONAL_STRING_FIELD,
    {
        "json-schema": {"pattern": TWITTER_PATTERN},
    })

MISSING_SUBJECT_ERROR = "Database error: missing object"


class ModelHelper(object):
    VALIDATORS = {}

    def __init__(self, subject):
        self.subject = subject
        self.errors = []
        if not self.subject:
            self.errors.append(MISSING_SUBJECT_ERROR)

    @classmethod
    def construct_object(cls, object_data):
        return cls.model.objects.create(**object_data)

    def serialize(self, fields):
        result = {}
        for field in fields:
            value = self.field_value(field)
            if value is not None:
                result[field] = value
        return result

    def field_value(self, field):
        if hasattr(self, field):
            return getattr(self, field)
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

    def list_of_field_elements(self, field, attribute):
        objects = getattr(self.subject, field, None)
        if objects:
            return [getattr(item, attribute, None) for item in objects.all()]

    def field_element(self, field, attribute):
        field_property = getattr(self.subject, field, None)
        return getattr(field_property, attribute, None)


def serialize_list_field(object, field, helper_class):
    if hasattr(object, field):
        result = []
        for item in getattr(object, field).all():
            helper = helper_class(item)
            result.append(helper.serialize(helper.fields()))
        return result


def json_object(properties):
    return {
        "type": "object",
        "properties": properties,
    }


def properties_from_fields(fields):
    result = {}
    for key, field in fields.items():
        result[key] = field["json-schema"]
    return result


def json_array(item):
    return {
        "type": "array",
        "item": item,
    }


def json_list_wrapper(item):
    return json_object({
        "count": RAW_INTEGER_FIELD,
        "next": RAW_URL_FIELD,
        "previous": RAW_URL_FIELD,
        "results": json_array(item)})


def json_simple_list(item, list_key):
    return json_object({list_key: json_array(item)})
