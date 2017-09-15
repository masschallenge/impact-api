from impact.v1.helpers.model_helper import ModelHelper


class OrganizationHelper(ModelHelper):
    REQUIRED_KEYS = [
        "name",
        "url_slug",
        ]
    OPTIONAL_KEYS = [
        "date_founded",
        "facebook_url",
        "full_elevator_pitch",
        "public_inquiry_email",
        "linked_in_url",
        "location_city",
        "location_national",
        "location_postcode",
        "location_regional",
        "short_pitch",
        "twitter_handle",
        "video_elevator_pitch_url",
        "website_url",
        ]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = [
        "id",
        "is_partner",
        "is_startup",
        "updated_at",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    def __init__(self, *args, **kwargs):
        super(OrganizationHelper, self).__init__(*args, **kwargs)
        self.startup = self.subject.startup_set.order_by("-id").first()
        self.partner = self.subject.partner_set.order_by("-id").first()

    @property
    def is_startup(self):
        return self.startup is not None

    @property
    def is_partner(self):
        return self.partner is not None

    def field_value(self, field):
        result = super(OrganizationHelper, self).field_value(field)
        if result is not None:
            return result
        if self.startup:
            result = getattr(self.startup, field, None)
        if result is not None:
            return result
        if self.partner:
            return getattr(self.partner, field, None)
