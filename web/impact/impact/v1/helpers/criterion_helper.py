# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import Criterion

from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    READ_ONLY_STRING_FIELD,
    REQUIRED_STRING_FIELD,
    STRING_FIELD,
)

CRITERION_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "type": REQUIRED_STRING_FIELD,
    "judging_round_id": INTEGER_FIELD,
}


class CriterionHelper(ModelHelper):
    model = Criterion

    @classmethod
    def fields(cls):
        return CRITERION_FIELDS
    
    
