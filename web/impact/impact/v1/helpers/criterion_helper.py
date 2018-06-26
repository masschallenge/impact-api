# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import Criterion

from impact.v1.helpers.model_helper import (
    REQUIRED_INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
)
ALL_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "type": REQUIRED_STRING_FIELD,
    "judging_round_id": REQUIRED_INTEGER_FIELD,
}


class CriterionHelper(ModelHelper):
    model = Criterion

    REQUIRED_KEYS = [
        "name",
        "type",
        "judging_round_id",
        ]
    ALL_KEYS = REQUIRED_KEYS
    INPUT_KEYS = ALL_KEYS

    @classmethod
    def fields(cls):
        return ALL_FIELDS
