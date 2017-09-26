from impact.models import Industry
from impact.v1.helpers.model_helper import ModelHelper
from impact.v1.metadata import (
    OPTIONAL_ID_TYPE,
    OPTIONAL_STRING_TYPE,
    PK_TYPE,
)


class IndustryHelper(ModelHelper):
    MODEL = Industry

    DETAIL_METADATA = {
        "id": PK_TYPE,
        "name": OPTIONAL_STRING_TYPE,
        "full_name": OPTIONAL_STRING_TYPE,
        "parent_id": OPTIONAL_ID_TYPE,
        }
    REQUIRED_KEYS = ["name"]
    OPTIONAL_KEYS = ["parent_id"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = ["id", "full_name"]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    @property
    def full_name(self):
        return str(self.subject)
