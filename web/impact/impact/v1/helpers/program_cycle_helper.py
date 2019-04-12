from accelerator.models import ProgramCycle
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    ModelHelper,
    OPTIONAL_STRING_FIELD,
    PK_FIELD,
)

PROGRAM_CYCLE_FIELDS = {
    "id": PK_FIELD,
    "name": OPTIONAL_STRING_FIELD,
    "short_name": OPTIONAL_STRING_FIELD,
    "applications_open": BOOLEAN_FIELD,
    "application_open_date": OPTIONAL_STRING_FIELD,
    "application_early_deadline_date": OPTIONAL_STRING_FIELD,
    "application_final_deadline_date": OPTIONAL_STRING_FIELD,
    "advertised_final_deadline": OPTIONAL_STRING_FIELD,
}


class ProgramCycleHelper(ModelHelper):
    model = ProgramCycle

    @classmethod
    def fields(cls):
        return PROGRAM_CYCLE_FIELDS
