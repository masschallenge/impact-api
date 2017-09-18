from impact.v1.helpers.model_helper import ModelHelper


class IndustryHelper(ModelHelper):
    REQUIRED_KEYS = ["name"]
    OPTIONAL_KEYS = ["parent_id"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = ["id", "full_name"]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    @property
    def full_name(self):
        return str(self.subject)
