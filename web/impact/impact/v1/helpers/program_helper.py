from accelerator.models import Program
from .model_helper import (
    ModelHelper,
    OPTIONAL_FLOAT_FIELD,
    OPTIONAL_INTEGER_FIELD,
    OPTIONAL_STRING_FIELD,
    PK_FIELD,
)

PROGRAM_FIELDS = {
    "id": PK_FIELD,
    "name": OPTIONAL_STRING_FIELD,
    "program_family_id": OPTIONAL_INTEGER_FIELD,
    "program_family_name": OPTIONAL_STRING_FIELD,
    "cycle_id": OPTIONAL_INTEGER_FIELD,
    "cycle_name": OPTIONAL_STRING_FIELD,
    "description": OPTIONAL_STRING_FIELD,
    "start_date": OPTIONAL_STRING_FIELD,
    "end_date": OPTIONAL_STRING_FIELD,
    "location": OPTIONAL_STRING_FIELD,
    "program_status": OPTIONAL_STRING_FIELD,
    "currency_code": OPTIONAL_STRING_FIELD,
    "regular_application_fee": OPTIONAL_FLOAT_FIELD,
    "url_slug": OPTIONAL_STRING_FIELD,
    "overview_start_date": OPTIONAL_STRING_FIELD,
    "overview_deadline_date": OPTIONAL_STRING_FIELD,
}


class ProgramHelper(ModelHelper):
    model = Program

    @classmethod
    def fields(cls):
        return PROGRAM_FIELDS

    @property
    def cycle_name(self):
        return self.field_element("cycle", "name")

    @property
    def program_family_name(self):
        return self.field_element("program_family", "name")
