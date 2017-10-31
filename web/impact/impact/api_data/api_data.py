# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from impact.models import (
    Program,
    Startup,
)


class APIData(object):
    """Argument parsing and validation methods."""
    INVALID_VALUE_MESSAGE = "'%s' is not a valid value for %s"
    NOT_FOUND_MESSAGE = "Value '%s' does not match any %s"
    YES = "Y"
    NO = "N"
    YES_NO_VALUES = [YES, NO]
    KEY_TO_CLASS_LOOKUP = {
        "ProgramKey": (Program, "name"),
        "StartupKey": (Startup, "organization__url_slug"),
    }

    def __init__(self, data, *args, **kwargs):
        self.errors = []
        self.data = data

    def record_invalid_value(self, value, field):
        self.errors.append(self.INVALID_VALUE_MESSAGE % (value, field))

    def record_not_found(self, value, field):
        self.errors.append(self.NOT_FOUND_MESSAGE % (value, field))

    def validate_field(self, field, valid_values):
        value = self.data.get(field, valid_values[0])
        if value in valid_values:
            return value
        self.record_invalid_value(value, field)
        return None

    def validate_program(self, required=True):
        return self._validate_object("ProgramKey", required)

    def validate_startup(self, required=True):
        return self._validate_object("StartupKey", required)

    def _validate_object(self, obj_key, required):
        key = self.data.get(obj_key, None)
        if key is None:
            if required:
                self.record_not_found(key, obj_key)
            return None
        result = self._lookup_object(key, obj_key)
        if not result:
            self.record_not_found(key, obj_key)
        return result

    def _lookup_object(self, key, obj_key):
        obj_class, lookup = self.KEY_TO_CLASS_LOOKUP[obj_key]
        result = None
        if isinstance(key, int) or key.isdigit():
            result = obj_class.objects.filter(id=key).first()
        elif isinstance(key, str):
            result = obj_class.objects.filter(**{lookup: key}).first()
        return result
