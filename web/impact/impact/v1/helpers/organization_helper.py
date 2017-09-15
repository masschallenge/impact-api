from impact.v1.helpers.model_helper import ModelHelper


class OrganizationHelper(ModelHelper):
    REQUIRED_KEYS = [
        "name",
        "url_slug",
        ]
    OPTIONAL_KEYS = [
        "public_inquiry_email",
        ]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = [
        "id",
        "is_partner",
        "is_startup",
        "updated_at",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    def field_value(self, field):
        if hasattr(self, field):
            return getattr(self, field)()
        return getattr(self.subject, field)

    def is_startup(self):
        return self.subject.startup_set.exists()

    def is_partner(self):
        return self.subject.partner_set.exists()
