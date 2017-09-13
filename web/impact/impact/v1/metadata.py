from rest_framework.metadata import SimpleMetadata


ORGANIZATION_ACTIONS = {
    'GET': {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "name": {
            "type": "string"
        },
        "url_slug": {
            "type": "string"
        },
        "public_inquiry_email": {
            "type": "string"
        },
        "is_startup": {
            "type": "boolean"
        },
        "is_partner": {
            "type": "boolean"
        },
        "updated_at": {
            "type": "string"
        }
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
        "name": {
            "type": "string"
        },
        "url_slug": {
            "type": "string"
        },
        "public_inquiry_email": {
            "type": "string"
        },
        "is_startup": {
            "type": "boolean"
        },
        "is_partner": {
            "type": "boolean"
        },
        "updated_at": {
            "type": "string"
        }
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
    "first_name": {
        "type": "string"
        },
    "last_name": {
        "type": "string"
        },
    "email": {
        "type": "string"
        },
    "is_active": {
        "type": "boolean"
        },
    "gender": {
        "type": "string"
        },
    "phone": {
        "type": "string"
        },
    "linked_in_url": {
        "type": "string"
        },
    "facebook_url": {
        "type": "string"
        },
    "twitter_handle": {
        "type": "string"
        },
    "personal_website_url": {
        "type": "string"
        }
}

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
