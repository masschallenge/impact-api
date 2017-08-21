from rest_framework.metadata import SimpleMetadata


ORGANIZATION_ACTIONS = {
    'POST': {
        'id': {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "name": {
            "type": "string",
            "required": True,
            "read_only": False,
            "label": "Name",
            "max_length": 225
        },
        "url_slug": {
            "type": "string",
            "required": True,
            "read_only": False,
            "label": "Name",
            "max_length": 225
        },
        "public_inquiry_email": {
            "type": "string",
            "required": True,
            "read_only": False,
            "label": "Name",
            "max_length": 225
        }
    },
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


USER_ACTIONS = {
    'GET': {
        "id": {
            "type": "integer",
            "required": False,
            "read_only": True,
            "label": "ID"
        },
        "first_name": {
            'type': 'string'
        },
        "last_name": {
            'type': 'string'
        },
        "email": {
            'type': 'string'
        },
        "is_active": {
            'type': 'boolean'
        },
        "gender": {
            "type": "string"
        },
        'organizations': {
            'type': 'list',
            "read_only": True,
        }
    }
}


class OrganizationMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata['actions'] = ORGANIZATION_ACTIONS

        return metadata


class UserMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata['actions'] = USER_ACTIONS

        return metadata


class UserOrganizationsMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata['actions'] = USER_ORGANIZATION_ACTIONS

        return metadata


class OrganizationUsersMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata['actions'] = ORGANIZATION_USER_ACTIONS

        return metadata
