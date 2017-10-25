from impact.models import Organization
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    EMAIL_FIELD,
    INTEGER_ARRAY_FIELD,
    INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    READ_ONLY_STRING_FIELD,
    REQUIRED_STRING_FIELD,
    STRING_FIELD,
    TWITTER_FIELD,
    URL_FIELD,
    URL_SLUG_FIELD,
    merge_fields,
)

STARTUP_FIELD = {
    "GET": {
        "included": "could_be_startup",
        "description": "This field exists only when is_startup is true",
    },
    "PATCH": {"allowed": "is_startup"},
    "POST": {"allowed": "could_be_startup"},
}
STARTUP_BOOLEAN_FIELD = merge_fields(STARTUP_FIELD, BOOLEAN_FIELD)
STARTUP_INTEGER_ARRAY_FIELD = merge_fields(STARTUP_FIELD, INTEGER_ARRAY_FIELD)
STARTUP_INTEGER_FIELD = merge_fields(STARTUP_FIELD, INTEGER_FIELD)
STARTUP_STRING_FIELD = merge_fields(STARTUP_FIELD, STRING_FIELD)
STARTUP_URL_FIELD = merge_fields(STARTUP_FIELD, URL_FIELD)

ORGANIZATION_FIELDS = {
    "id": PK_FIELD,
    "is_partner": BOOLEAN_FIELD,
    "is_startup": BOOLEAN_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "public_inquiry_email": EMAIL_FIELD,
    "twitter_handle": TWITTER_FIELD,
    "updated_at": READ_ONLY_STRING_FIELD,
    "url_slug": URL_SLUG_FIELD,
    "website_url": URL_FIELD,

    # Startup specific fields
    "additional_industry_ids": STARTUP_INTEGER_ARRAY_FIELD,
    "date_founded": STARTUP_STRING_FIELD,
    "facebook_url": STARTUP_URL_FIELD,
    "full_elevator_pitch": STARTUP_STRING_FIELD,
    "is_visible": STARTUP_BOOLEAN_FIELD,
    "linked_in_url": STARTUP_URL_FIELD,
    "location_city": STARTUP_STRING_FIELD,
    "location_national": STARTUP_STRING_FIELD,
    "location_postcode": STARTUP_STRING_FIELD,
    "location_regional": STARTUP_STRING_FIELD,
    "primary_industry_id": STARTUP_INTEGER_FIELD,
    "short_pitch": STARTUP_STRING_FIELD,
    "video_elevator_pitch_url": STARTUP_URL_FIELD,
}

ORGANIZATION_USERS_FIELDS = {
    "id": PK_FIELD,
    "startup_administrator": BOOLEAN_FIELD,
    "partner_administrator": BOOLEAN_FIELD,
    "primary_contact": BOOLEAN_FIELD,
}


class OrganizationHelper(ModelHelper):
    MODEL = Organization

    REQUIRED_KEYS = [
        "name",
        "url_slug",
        ]
    OPTIONAL_KEYS = [
        "additional_industry_ids",
        "date_founded",
        "facebook_url",
        "full_elevator_pitch",
        "primary_industry_id",
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
        super().__init__(*args, **kwargs)
        self.startup = self.subject.startup_set.order_by("-id").first()
        self.partner = self.subject.partner_set.order_by("-id").first()

    @property
    def is_startup(self):
        return self.startup is not None

    @property
    def is_partner(self):
        return self.partner is not None

    @property
    def additional_industry_ids(self):
        if self.startup:
            categories = self.startup.additional_industries
            if categories.exists():
                return list(categories.values_list("id", flat=True))

    def field_value(self, field):
        result = super().field_value(field)
        if result is None and self.startup:
            result = getattr(self.startup, field, None)
        if result is None and self.partner:
            result = getattr(self.partner, field, None)
        return result
