from impact.v1.helpers.model_helper import (
    json_object,
    ModelHelper,
    PK_FIELD,
    properties_from_fields,
    READ_ONLY_ID_FIELD,
    READ_ONLY_STRING_FIELD,
    REQUIRED_STRING_FIELD,
)

MPTT_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "full_name": READ_ONLY_STRING_FIELD,
    "parent_id": READ_ONLY_ID_FIELD,
}
MPTT_TYPE = json_object(properties_from_fields(MPTT_FIELDS))


class MPTTModelHelper(ModelHelper):
    OPTIONAL_KEYS = ["parent_id"]
    REQUIRED_KEYS = ["name"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    @classmethod
    def fields(cls):
        return MPTT_FIELDS

    @property
    def full_name(self):
        return str(self.subject)
