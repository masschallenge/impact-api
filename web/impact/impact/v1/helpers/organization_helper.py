# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

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
    json_array,
    json_schema,
    merge_fields,
    serialize_list_field,
)
from impact.v1.helpers.industry_helper import (
    INDUSTRY_TYPE,
    IndustryHelper,
)

COULD_BE_STARTUP_CHECK = "could_be_startup"
IS_STARTUP_CHECK = "is_startup"
STARTUP_FIELD = {
    "GET": {
        "included": COULD_BE_STARTUP_CHECK,
        "description": "This field exists only when is_startup is true",
    },
    "PATCH": {"allowed": IS_STARTUP_CHECK},
    "POST": {"allowed": COULD_BE_STARTUP_CHECK},
}
STARTUP_BOOLEAN_FIELD = merge_fields(STARTUP_FIELD, BOOLEAN_FIELD)
STARTUP_INTEGER_ARRAY_FIELD = merge_fields(STARTUP_FIELD, INTEGER_ARRAY_FIELD)
STARTUP_INTEGER_FIELD = merge_fields(STARTUP_FIELD, INTEGER_FIELD)
STARTUP_STRING_FIELD = merge_fields(STARTUP_FIELD, STRING_FIELD)
STARTUP_URL_FIELD = merge_fields(STARTUP_FIELD, URL_FIELD)
STARTUP_INDUSTRY_FIELD = merge_fields(STARTUP_FIELD,
                                      json_schema(INDUSTRY_TYPE))
STARTUP_INDUSTRY_ARRAY_FIELD = merge_fields(
    STARTUP_FIELD, json_schema(json_array(INDUSTRY_TYPE)))
ORGANIZATION_URL_SLUG_FIELD = merge_fields(
    STRING_FIELD, {"json-schema": {"pattern": "^[a-zA-Z0-9-]+$"}})

ORGANIZATION_FIELDS = {
    "id": PK_FIELD,
    "is_partner": BOOLEAN_FIELD,
    "is_startup": BOOLEAN_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "public_inquiry_email": EMAIL_FIELD,
    "twitter_handle": TWITTER_FIELD,
    "updated_at": READ_ONLY_STRING_FIELD,
    "url_slug": ORGANIZATION_URL_SLUG_FIELD,
    "website_url": URL_FIELD,

    # Startup specific fields
    "additional_industries": STARTUP_INDUSTRY_ARRAY_FIELD,
    "date_founded": STARTUP_STRING_FIELD,
    "facebook_url": STARTUP_URL_FIELD,
    "full_elevator_pitch": STARTUP_STRING_FIELD,
    "is_visible": STARTUP_BOOLEAN_FIELD,
    "linked_in_url": STARTUP_URL_FIELD,
    "location_city": STARTUP_STRING_FIELD,
    "location_national": STARTUP_STRING_FIELD,
    "location_postcode": STARTUP_STRING_FIELD,
    "location_regional": STARTUP_STRING_FIELD,
    "primary_industry": STARTUP_INDUSTRY_FIELD,
    "short_pitch": STARTUP_STRING_FIELD,
    "video_elevator_pitch_url": STARTUP_URL_FIELD,
}

ORGANIZATION_USER_FIELDS = {
    "id": PK_FIELD,
    "startup_administrator": BOOLEAN_FIELD,
    "partner_administrator": BOOLEAN_FIELD,
    "primary_contact": BOOLEAN_FIELD,
}


class OrganizationHelper(ModelHelper):
    model = Organization

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startup = self.subject.startup_set.order_by("-id").first()
        self.partner = self.subject.partner_set.order_by("-id").first()

    @classmethod
    def fields(cls):
        return ORGANIZATION_FIELDS

    @property
    def is_startup(self):
        return self.startup is not None

    @property
    def is_partner(self):
        return self.partner is not None

    @property
    def additional_industries(self):
        return serialize_list_field(self.startup,
                                    "additional_industries",
                                    IndustryHelper)

    @property
    def primary_industry(self):
        if self.startup:
            helper = IndustryHelper(self.startup.primary_industry)
            return helper.serialize(helper.fields())

    def field_value(self, field):
        result = super().field_value(field)
        if result is None and self.startup:
            result = getattr(self.startup, field, None)
        if result is None and self.partner:
            result = getattr(self.partner, field, None)
        return result
