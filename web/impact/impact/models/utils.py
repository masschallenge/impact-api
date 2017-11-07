# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


import re


LABEL_LENGTH = 255


def is_managed(db_table):
    return False


def split_on_caps(value):
    original_model_string = re.findall('[A-Z][^A-Z]*', value)
    holder = ""
    for word in original_model_string:
        holder += word.lower() + "_"
        new_model_string = holder[:-1]
    return new_model_string


def snake_to_camel_case(value):
    old_value = value.split('_')
    new_value = ""
    for word in old_value:
        new_value += (word[0].upper() + word[1:])
    return new_value
