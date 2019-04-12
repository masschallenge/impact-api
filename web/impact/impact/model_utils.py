# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.core.exceptions import FieldDoesNotExist
from django.utils.text import camel_case_to_spaces

LABEL_LENGTH = 255


def model_has_field(model, field_name):
    try:
        model._meta.get_field(field_name)
        return True
    except FieldDoesNotExist:
        return False


def model_name_to_snake(value):
    original_model_string = camel_case_to_spaces(value)
    new_model_string = original_model_string.replace(" ", "_")
    return new_model_string


def snake_to_model_name(value):
    return "".join(map(str.title, value.split("_")))


def is_int(s):
    try:
        int(str(s))
    except ValueError:
        return False
    return True
