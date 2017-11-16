# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from impact.tests.factories import ProgramFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.views import ProgramDetailView

PROGRAM_GET_FIELDS = [
    "id",
    "name",
    "program_family_id",
    "program_family_name",
    "cycle_id",
    "cycle_name",
    "description",
    "start_date",
    "end_date",
    "location",
    "currency_code",
    "regular_application_fee",
    "url_slug",
    "overview_start_date",
    "overview_deadline_date",
]


class TestProgramDetailView(APITestCase):
    def test_get(self):
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ProgramDetailView.view_name,
                          args=[program.id])
            response = self.client.get(url)
            assert response.data["name"] == program.name
            assert response.data["cycle_name"] == program.cycle.name
            assert (response.data["program_family_name"] ==
                    program.program_family.name)

    def test_options(self):
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ProgramDetailView.view_name,
                          args=[program.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(PROGRAM_GET_FIELDS, get_options)

    def test_options_against_get(self):
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ProgramDetailView.view_name,
                          args=[program.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
