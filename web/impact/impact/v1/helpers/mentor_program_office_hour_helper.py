# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

from accelerator.models import MentorProgramOfficeHour
from impact.v1.helpers.model_helper import (
    ModelHelper,
    PK_FIELD,
    OPTIONAL_STRING_FIELD,
)

OFFFICE_HOUR_FIELDS = {
    "id": PK_FIELD,
    "title": OPTIONAL_STRING_FIELD,
    "location": OPTIONAL_STRING_FIELD,
    "start_time": OPTIONAL_STRING_FIELD,
    "end_time": OPTIONAL_STRING_FIELD,
    "date": OPTIONAL_STRING_FIELD,
    "mentor_name": OPTIONAL_STRING_FIELD,
    "mentor_email": OPTIONAL_STRING_FIELD,
    "finalist_name": OPTIONAL_STRING_FIELD,
    "finalist_email": OPTIONAL_STRING_FIELD,
}


class MentorProgramOfficeHourHelper(ModelHelper):
    model = MentorProgramOfficeHour

    @classmethod
    def fields(cls):
        return OFFFICE_HOUR_FIELDS

    @property
    def title(self):
        return str(self.subject)

    @property
    def mentor_name(self):
        return self.subject.mentor.full_name()

    @property
    def mentor_email(self):
        return self.field_element("mentor", "email")

    @property
    def finalist_name(self):
        return self.subject.finalist.full_name()

    @property
    def finalist_email(self):
        return self.field_element("finalist", "email")
