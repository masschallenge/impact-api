# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import Application
from impact.v1.helpers.model_helper import (
    ModelHelper,
    OPTIONAL_INTEGER_FIELD,
    OPTIONAL_STRING_FIELD,
    PK_FIELD,
)

APPLICATION_FIELDS = {
    "application_status": OPTIONAL_STRING_FIELD,
    "application_type": OPTIONAL_INTEGER_FIELD,
    "created_at": OPTIONAL_STRING_FIELD,
    "cycle": OPTIONAL_INTEGER_FIELD,
    "id": PK_FIELD,
    "startup": OPTIONAL_INTEGER_FIELD,
    "submission_datetime": OPTIONAL_STRING_FIELD,
    "updated_at": OPTIONAL_STRING_FIELD,
}


class ApplicationHelper(ModelHelper):
    model = Application

    @classmethod
    def fields(cls):
        return APPLICATION_FIELDS

    @property
    def application_type(self):
        return self.field_element("application_type", "id")

    @property
    def cycle(self):
        return self.field_element("cycle", "id")

    @property
    def startup(self):
        return self.field_element("startup", "id")
