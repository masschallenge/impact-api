# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from accelerator.models import CriterionOptionSpec

from .model_helper import (
    ModelHelper,
    OPTIONAL_FLOAT_FIELD,
    OPTIONAL_INTEGER_FIELD,
    PK_FIELD,
    REQUIRED_INTEGER_FIELD,
    REQUIRED_STRING_FIELD,
)
from .criterion_helper import CriterionHelper
from .validators import (
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
    '''Encapsulates business logic for CriterionOptionSpecs, including logic
    around allocation, analysis, and cloning.
    '''
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

    def __init__(self, subject, criterion_helpers=None):
        super().__init__(subject)
        criterion = subject.criterion
        if criterion_helpers is not None:
            self.criterion_helper = criterion_helpers.get(criterion.id)
        else:
            CriterionHelper.find_helper(criterion)

    def options(self, apps):
        return self.criterion_helper.options(self.subject, apps)

    def app_count(self, apps, option_name):
        return self.criterion_helper.app_count(apps, option_name)

    @classmethod
    def fields(cls):
        return CRITERION_OPTION_SPEC_FIELDS

    @classmethod
    def clone_option_specs(cls, clones):
        for original_id, copy_id in clones:
            cls.clone_options(original_id, copy_id)

    @classmethod
    def clone_options(cls, original_id, copy_id):
        option_specs = cls.model.objects.filter(criterion_id=original_id)
        cls.model.objects.bulk_create([
            cls.model(option=spec.option,
                      count=spec.count,
                      weight=spec.weight,
                      criterion_id=copy_id)
            for spec in option_specs])
