# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models import RefundCode
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    INTEGER_ARRAY_FIELD,
    INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    STRING_FIELD,
)


PROGRAMS_FIELD = {
    "json-schema": {
        "type": "array",
        "items": {"type": "string"},
    },
    "POST": {"required": False},
    "PATCH": {"required": False},
}

CREDIT_CODE_FIELDS = {
    "id": PK_FIELD,
    "issued_to": INTEGER_FIELD,
    "created_at": STRING_FIELD,
    "unique_code": STRING_FIELD,
    "discount": INTEGER_FIELD,
    "maximum_uses": INTEGER_FIELD,
    "programs": INTEGER_ARRAY_FIELD,
    "notes": STRING_FIELD,
    "internal": BOOLEAN_FIELD,
}


class CreditCodeHelper(ModelHelper):
    model = RefundCode

    @classmethod
    def fields(self):
        return CREDIT_CODE_FIELDS

    @property
    def issued_to(self):
        return self.get_field_value("issued_to").pk

    @property
    def programs(self):
        programs = self.get_field_value("programs")
        if programs:
            return [program.pk for program in programs.all()]
