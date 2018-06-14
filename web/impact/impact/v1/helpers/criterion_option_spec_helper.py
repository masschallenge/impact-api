# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import CriterionOptionSpec

from impact.v1.helpers.model_helper import (
    INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
    STRING_FIELD,
)

CRITERION_OPTION_SPEC_FIELDS = {
    "id": PK_FIELD,
    "option": REQUIRED_STRING_FIELD,
    "count": STRING_FIELD,
    "weight": STRING_FIELD,    
    "criterion_id": INTEGER_FIELD,
}


class CriterionOptionSpecHelper(ModelHelper):
    model = CriterionOptionSpec

    @classmethod
    def fields(cls):
        return CRITERION_OPTION_SPEC_FIELDS
    
    
