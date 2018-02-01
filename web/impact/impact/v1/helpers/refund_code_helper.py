# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models import RefundCode
from impact.v1.helpers.model_helper import(
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

REFUND_CODE_FIELDS = {
    "id": PK_FIELD,
    "issued_to": INTEGER_FIELD,
    "created_at": STRING_FIELD,
    "unique_code": STRING_FIELD,
    "discount": INTEGER_FIELD,
    "maximum_uses": INTEGER_FIELD,
    "programs": INTEGER_ARRAY_FIELD,
}


class RefundCodeHelper(ModelHelper):
    model = RefundCode

    @classmethod
    def fields(self):
        return REFUND_CODE_FIELDS

    @property
    def issued_to(self):
        return self.field_pk("issued_to")

    @property
    def programs(self):
        if hasattr(self.subject, "programs"):
            programs = self.subject.programs
            if programs:
                return [program.pk for program in programs.all()]

