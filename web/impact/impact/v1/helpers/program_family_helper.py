import re
from impact.models import ProgramFamily
from impact.v1.helpers.model_helper import (
    ModelHelper,
    PHONE_FIELD,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
    STRING_FIELD,
    URL_SLUG_FIELD,
)

EMAIL_DOMAIN_PATTERN = '^[a-z][a-z.]+[a-z]$'
EMAIL_DOMAIN_REGEX = re.compile(EMAIL_DOMAIN_PATTERN)
EMAIL_DOMAIN_FIELD = {
    "json-schema": {
        "type": "string",
        "pattern": EMAIL_DOMAIN_PATTERN,
    },
    "PATCH": {"required": False},
    "POST": {"required": False},
}

PROGRAM_FAMILY_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "email_domain": EMAIL_DOMAIN_FIELD,
    "phone_number": PHONE_FIELD,
    "short_description": STRING_FIELD,
    "url_slug": URL_SLUG_FIELD,
}


class ProgramFamilyHelper(ModelHelper):
    model = ProgramFamily
    REQUIRED_KEYS = ["name"]
    OPTIONAL_KEYS = ["email_domain",
                     "phone_number",
                     "short_description",
                     "url_slug"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    @classmethod
    def fields(cls):
        return PROGRAM_FAMILY_FIELDS
