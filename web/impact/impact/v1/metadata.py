from rest_framework.metadata import SimpleMetadata
from impact.v1.helpers import ProfileHelper


OPTIONAL_STRING_TYPE = {"type": "string"}
OPTIONAL_BOOLEAN_TYPE = {"type": "string"}

ORGANIZATION_ACTIONS = {
    'GET': {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "name": OPTIONAL_STRING_TYPE,
        "url_slug": OPTIONAL_STRING_TYPE,
        "public_inquiry_email": OPTIONAL_STRING_TYPE,
        "is_startup": OPTIONAL_BOOLEAN_TYPE,
        "is_partner": OPTIONAL_BOOLEAN_TYPE,
        "updated_at": OPTIONAL_STRING_TYPE
    }
}

ORGANIZATION_DETAIL_ACTIONS = {
    'GET': {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "name": OPTIONAL_STRING_TYPE,
        "url_slug": OPTIONAL_STRING_TYPE,
        "public_inquiry_email": OPTIONAL_STRING_TYPE,
        "is_startup": OPTIONAL_BOOLEAN_TYPE,
        "is_partner": OPTIONAL_BOOLEAN_TYPE,
        "updated_at": OPTIONAL_STRING_TYPE
    }
}

ORGANIZATION_HISTORY_ACTIONS = {
    "GET": {
        "history": {
            "type": "field",
            "read_only": True,
        }
    }
}

USER_HISTORY_ACTIONS = {
    "GET": {
        "history": {
            "type": "field",
            "read_only": True,
        }
    }
}

USER_ORGANIZATION_ACTIONS = {
    'GET': {
        'organizations': {
            'type': 'list',
            "read_only": True,
        }
    }
}

ORGANIZATION_USER_ACTIONS = {
    'GET': {
        'users': {
            'type': 'list',
            "read_only": True,
        }
    }
}


USER_POST_OPTIONS = {
    "first_name": OPTIONAL_STRING_TYPE,
    "last_name": OPTIONAL_STRING_TYPE,
    "email": OPTIONAL_STRING_TYPE,
    "is_active": OPTIONAL_BOOLEAN_TYPE,
    "gender": OPTIONAL_STRING_TYPE,
    "phone": OPTIONAL_STRING_TYPE,
}
USER_POST_OPTIONS.update(dict([(key, OPTIONAL_STRING_TYPE)
                               for key in ProfileHelper.OPTIONAL_KEYS]))

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
    'Organization Detail': ORGANIZATION_DETAIL_ACTIONS,
    'Organization History': ORGANIZATION_HISTORY_ACTIONS,
    'Organization List': ORGANIZATION_ACTIONS,
    'Organization Users': ORGANIZATION_USER_ACTIONS,
    'User Detail': USER_DETAIL_ACTIONS,
    'User List': USER_ACTIONS,
    'User Organizations': USER_ORGANIZATION_ACTIONS,
    'User History': USER_HISTORY_ACTIONS,
}


class ImpactMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        view_name = view.get_view_name()
        metadata = super().determine_metadata(request, view)
        metadata['actions'] = METADATA_MAP.get(view_name)

        return metadata
