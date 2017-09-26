from impact.models import Organization
from impact.v1.helpers.model_helper import ModelHelper
from impact.v1.metadata import (
    OPTIONAL_STRING_TYPE,
    OPTIONAL_BOOLEAN_TYPE,
    OPTIONAL_DATE_TYPE,
    OPTIONAL_LIST_TYPE,
    OPTIONAL_ID_TYPE,
    PK_TYPE,
)


class OrganizationHelper(ModelHelper):
    MODEL = Organization

    DETAIL_METADATA = {
        "id": PK_TYPE,
        "name": OPTIONAL_STRING_TYPE,
        "url_slug": OPTIONAL_STRING_TYPE,
        "additional_industry_ids": OPTIONAL_LIST_TYPE,
        "date_founded": OPTIONAL_DATE_TYPE,
        "facebook_url": OPTIONAL_STRING_TYPE,
        "full_elevator_pitch": OPTIONAL_STRING_TYPE,
        "primary_industry_id": OPTIONAL_ID_TYPE,
        "public_inquiry_email": OPTIONAL_STRING_TYPE,
        "linked_in_url": OPTIONAL_STRING_TYPE,
        "location_city": OPTIONAL_STRING_TYPE,
        "location_national": OPTIONAL_STRING_TYPE,
        "location_postcode": OPTIONAL_STRING_TYPE,
        "location_regional": OPTIONAL_STRING_TYPE,
        "short_pitch": OPTIONAL_STRING_TYPE,
        "twitter_handle": OPTIONAL_STRING_TYPE,
        "video_elevator_pitch_url": OPTIONAL_STRING_TYPE,
        "website_url": OPTIONAL_STRING_TYPE,
        "is_startup": OPTIONAL_BOOLEAN_TYPE,
        "is_partner": OPTIONAL_BOOLEAN_TYPE,
        "updated_at": OPTIONAL_DATE_TYPE,
    }
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
        super(OrganizationHelper, self).__init__(*args, **kwargs)
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
            categories = self.startup.additional_industry_categories
            if categories.exists():
                return list(categories.values_list("id", flat=True))

    def field_value(self, field):
        result = super(OrganizationHelper, self).field_value(field)
        if result is None and self.startup:
            result = getattr(self.startup, field, None)
        if result is None and self.partner:
            result = getattr(self.partner, field, None)
        return result
