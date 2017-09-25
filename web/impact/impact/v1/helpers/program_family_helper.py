from impact.models import ProgramFamily
from impact.v1.helpers.model_helper import ModelHelper
from impact.v1.metadata import (
    OPTIONAL_ID_TYPE,
    OPTIONAL_STRING_TYPE,
    PK_TYPE,
)


class ProgramFamilyHelper(ModelHelper):
    MODEL = ProgramFamily

    DETAIL_METADATA = {
        "id": PK_TYPE,
        "name": OPTIONAL_STRING_TYPE,
        "email_domain": OPTIONAL_STRING_TYPE,
        "phone_number": OPTIONAL_STRING_TYPE,
        "short_description": OPTIONAL_STRING_TYPE,
        "url_slug": OPTIONAL_STRING_TYPE,
        }

    REQUIRED_KEYS = ["name"]
    OPTIONAL_KEYS = ["email_domain",
                     "phone_number",
                     "short_description",
                     "url_slug"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = ["id"]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    @property
    def full_name(self):
        return str(self.subject)
