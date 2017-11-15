from impact.models import ProgramCycle
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    ModelHelper,
    PK_FIELD,
    STRING_FIELD,
)

PROGRAM_CYCLE_FIELDS = {
    "id": PK_FIELD,
    "name": STRING_FIELD,
    "short_name": STRING_FIELD,
    "applications_open": BOOLEAN_FIELD,
    "application_open_date": STRING_FIELD,
    "application_early_deadline_date": STRING_FIELD,
    "application_final_deadline_date": STRING_FIELD,
    "advertised_final_deadline": STRING_FIELD,
}


class ProgramCycleHelper(ModelHelper):
    model = ProgramCycle

    @classmethod
    def fields(cls):
        return PROGRAM_CYCLE_FIELDS
