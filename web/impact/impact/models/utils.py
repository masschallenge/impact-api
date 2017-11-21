# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import re
from django.core.exceptions import FieldDoesNotExist
from django.utils.text import camel_case_to_spaces


LABEL_LENGTH = 255


def is_managed(db_table):
    return False


def model_has_field(model, field_name):
    try:
        model._meta.get_field(field_name)
        return True
    except FieldDoesNotExist:
        return False
