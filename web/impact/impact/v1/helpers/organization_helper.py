from impact.v1.helpers.model_helper import ModelHelper

REQUIRED_ORG_KEYS = [
    "name",
    "url_slug",
]
OPTIONAL_ORG_KEYS = [
    "public_inquiry_email",
]
INPUT_ORG_KEYS = REQUIRED_ORG_KEYS + OPTIONAL_ORG_KEYS

READ_ONLY_ORG_KEYS = [
    "id",
    "updated_at",
]
OUTPUT_ORG_KEYS = READ_ONLY_ORG_KEYS + INPUT_ORG_KEYS


class OrganizationHelper(ModelHelper):
    def __init__(self, organization):
        self.subject = organization

    OUTPUT_KEYS = OUTPUT_ORG_KEYS

    def serialize(self):
        result = super(OrganizationHelper, self).serialize()
        result["is_startup"] = self.is_startup()
        result["is_partner"] = self.is_partner()
        return result

    def is_startup(self):
        return self.subject.startup_set.exists()

    def is_partner(self):
        return self.subject.partner_set.exists()
