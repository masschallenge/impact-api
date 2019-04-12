# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import RefundCode
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    INTEGER_ARRAY_FIELD,
    OPTIONAL_INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    OPTIONAL_STRING_FIELD,
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
    "issued_to": OPTIONAL_INTEGER_FIELD,
    "created_at": OPTIONAL_STRING_FIELD,
    "unique_code": OPTIONAL_STRING_FIELD,
    "discount": OPTIONAL_INTEGER_FIELD,
    "maximum_uses": OPTIONAL_INTEGER_FIELD,
    "programs": INTEGER_ARRAY_FIELD,
    "notes": OPTIONAL_STRING_FIELD,
    "internal": BOOLEAN_FIELD,
}


class CreditCodeHelper(ModelHelper):
    model = RefundCode

    @classmethod
    def fields(cls):
        return CREDIT_CODE_FIELDS

    @property
    def issued_to(self):
        return self.field_element("issued_to", "pk")

    @property
    def programs(self):
        return self.list_of_field_elements("programs", "pk")
