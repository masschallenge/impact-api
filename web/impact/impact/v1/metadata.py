from rest_framework.metadata import SimpleMetadata
from impact.v1.helpers import ProfileHelper


OPTIONAL_STRING_TYPE = {"type": "string"}
OPTIONAL_BOOLEAN_TYPE = {"type": "boolean"}
OPTIONAL_DATE_TYPE = OPTIONAL_STRING_TYPE
OPTIONAL_LIST_TYPE = {"type": "field"}
OPTIONAL_ID_TYPE = {"type": "integer"}
READ_ONLY_LIST_TYPE = {"type": "field", "read_only": True}


INDUSTRY_DETAIL_ACTIONS = {
    "GET": {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "name": OPTIONAL_STRING_TYPE,
        "full_name": OPTIONAL_STRING_TYPE,
        "parent_id": OPTIONAL_ID_TYPE,
    }
}
INDUSTRY_ACTIONS = INDUSTRY_DETAIL_ACTIONS

ORGANIZATION_DETAIL_ACTIONS = {
    "GET": {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
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
        "updated_at": OPTIONAL_DATE_TYPE
    }
}

ORGANIZATION_ACTIONS = ORGANIZATION_DETAIL_ACTIONS

ORGANIZATION_HISTORY_ACTIONS = {
    "GET": {"history": READ_ONLY_LIST_TYPE}
}

USER_HISTORY_ACTIONS = {
    "GET": {"history": READ_ONLY_LIST_TYPE}
}

USER_ORGANIZATION_ACTIONS = {
    "GET": {"organizations": READ_ONLY_LIST_TYPE}
}

ORGANIZATION_USER_ACTIONS = {
    "GET": {"users": READ_ONLY_LIST_TYPE}
}


USER_POST_OPTIONS = {
    "first_name": OPTIONAL_STRING_TYPE,
    "last_name": OPTIONAL_STRING_TYPE,
    "email": OPTIONAL_STRING_TYPE,
    "is_active": OPTIONAL_BOOLEAN_TYPE,
    "gender": OPTIONAL_STRING_TYPE,
    "phone": OPTIONAL_STRING_TYPE,
    "additional_industry_ids": OPTIONAL_LIST_TYPE,
    "expert_category": OPTIONAL_STRING_TYPE,
    "mentoring_specialties": OPTIONAL_LIST_TYPE,
    "primary_industry_id": OPTIONAL_ID_TYPE,
    "updated_at": OPTIONAL_DATE_TYPE,
}
USER_POST_OPTIONS.update(dict([
            (key, OPTIONAL_BOOLEAN_TYPE)
            for key in ProfileHelper.OPTIONAL_BOOLEAN_KEYS]))
USER_POST_OPTIONS.update(dict([
            (key, OPTIONAL_STRING_TYPE)
            for key in ProfileHelper.OPTIONAL_STRING_KEYS]))

USER_GET_OPTIONS = USER_POST_OPTIONS.copy()
USER_GET_OPTIONS.update(
    {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "updated_at": {
            "type": "string",
            "read_only": True
        },
        "last_login": {
            "type": "string",
            "read_only": True
        },
        "date_joined": {
            "type": "string",
            "read_only": True
        },
    })


USER_ACTIONS = {
    "GET": USER_GET_OPTIONS,
    "POST": USER_POST_OPTIONS,
}


USER_DETAIL_ACTIONS = {
    "GET": USER_GET_OPTIONS,
    "PATCH": USER_POST_OPTIONS,
}


METADATA_MAP = {
    "Industry Detail": INDUSTRY_DETAIL_ACTIONS,
    "Industry List": INDUSTRY_ACTIONS,
    "Organization Detail": ORGANIZATION_DETAIL_ACTIONS,
    "Organization History": ORGANIZATION_HISTORY_ACTIONS,
    "Organization List": ORGANIZATION_ACTIONS,
    "Organization Users": ORGANIZATION_USER_ACTIONS,
    "User Detail": USER_DETAIL_ACTIONS,
    "User List": USER_ACTIONS,
    "User Organizations": USER_ORGANIZATION_ACTIONS,
    "User History": USER_HISTORY_ACTIONS,
}


class ImpactMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        view_name = view.get_view_name()
        metadata = super().determine_metadata(request, view)
        metadata["actions"] = METADATA_MAP.get(view_name)

        return metadata
