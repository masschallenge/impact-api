# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import CriterionOptionSpec

from impact.v1.helpers.model_helper import (
    REQUIRED_INTEGER_FIELD,
    ModelHelper,
    OPTIONAL_FLOAT_FIELD,
    OPTIONAL_INTEGER_FIELD,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
)
from impact.v1.helpers.validators import (
    validate_string,
    validate_integer,
    validate_float,
)
CRITERION_OPTION_SPEC_FIELDS = {
    "id": PK_FIELD,
    "option": REQUIRED_STRING_FIELD,
    "count": OPTIONAL_INTEGER_FIELD,
    "weight": OPTIONAL_FLOAT_FIELD,
    "criterion_id": REQUIRED_INTEGER_FIELD,
}


class CriterionOptionSpecHelper(ModelHelper):
    model = CriterionOptionSpec
    VALIDATORS = {
        "option": validate_string,
        "count": validate_integer,
        "weight": validate_float,
        "criterion_id": validate_integer,
        }

    REQUIRED_KEYS = [
        "option",
        "criterion_id",
        ]
    ALL_KEYS = REQUIRED_KEYS + [
        "count",
        "weight",
    ]
    INPUT_KEYS = ALL_KEYS

    @classmethod
    def fields(cls):
        return CRITERION_OPTION_SPEC_FIELDS
