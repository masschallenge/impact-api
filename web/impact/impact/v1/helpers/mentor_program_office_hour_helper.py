# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

from mc.models import MentorProgramOfficeHour
from .model_helper import (
    ModelHelper,
    BOOLEAN_FIELD,
    OPTIONAL_INTEGER_FIELD,
    OPTIONAL_STRING_FIELD,
    PK_FIELD,
)

OFFFICE_HOUR_FIELDS = {
    "id": PK_FIELD,
    "title": OPTIONAL_STRING_FIELD,
    "location": OPTIONAL_STRING_FIELD,
    "timezone": OPTIONAL_STRING_FIELD,
    "start_date_time": OPTIONAL_STRING_FIELD,
    "end_date_time": OPTIONAL_STRING_FIELD,
    "mentor_id": OPTIONAL_INTEGER_FIELD,
    "mentor_name": OPTIONAL_STRING_FIELD,
    "mentor_email": OPTIONAL_STRING_FIELD,
    "finalist_id": OPTIONAL_INTEGER_FIELD,
    "finalist_name": OPTIONAL_STRING_FIELD,
    "finalist_email": OPTIONAL_STRING_FIELD,
    "is_open": BOOLEAN_FIELD,
    "topics": OPTIONAL_STRING_FIELD,
    "description": OPTIONAL_STRING_FIELD,
    "street_address": OPTIONAL_STRING_FIELD,
    "city": OPTIONAL_STRING_FIELD,
    "state": OPTIONAL_STRING_FIELD,
    "program_family": OPTIONAL_STRING_FIELD,
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
    def program_family(self):
        return self.subject.program.program_family.name

    @property
    def location(self):
        return self.field_element("location", "name")

    @property
    def street_address(self):
        return self.field_element("location", "street_address")

    @property
    def city(self):
        return self.field_element("location", "city")

    @property
    def state(self):
        return self.field_element("location", "state")

    @property
    def timezone(self):
        return self.field_element("location", "timezone")

    @property
    def mentor_id(self):
        return self.field_element("mentor", "id")

    @property
    def mentor_name(self):
        return self.subject.mentor.full_name()

    @property
    def mentor_email(self):
        return self.field_element("mentor", "email")

    @property
    def finalist_id(self):
        return self.field_element("finalist", "id")

    @property
    def finalist_name(self):
        return self.subject.finalist.full_name()

    @property
    def finalist_email(self):
        return self.field_element("finalist", "email")

    @property
    def is_open(self):
        return self.subject.is_open()

    @property
    def topics(self):
        return self.subject.topics

    @property
    def description(self):
        return self.subject.description
