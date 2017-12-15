# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models import FunctionalExpertise
from impact.v1.helpers.model_helper import (
    ModelHelper,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
    READ_ONLY_ID_FIELD,
    READ_ONLY_STRING_FIELD,
    json_object,
    properties_from_fields,
)

FUNCTIONAL_EXPERTISE_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "full_name": READ_ONLY_STRING_FIELD,
    "parent_id": READ_ONLY_ID_FIELD,
}
# INDUSTRY_TYPE = json_object(properties_from_fields(INDUSTRY_FIELDS))


class FunctionalExpertiseHelper(ModelHelper):
    model = FunctionalExpertise

    REQUIRED_KEYS = ["name"]
    OPTIONAL_KEYS = ["parent_id"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    @property
    def full_name(self):
        return str(self.subject)

    @classmethod
    def fields(cls):
        return FUNCTIONAL_EXPERTISE_FIELDS
