# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from impact.tests.factories import ProgramFamilyFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.views import ProgramFamilyDetailView

PROGRAM_FAMILY_GET_FIELDS = [
    "id",
    "name",
    "email_domain",
    "phone_number",
    "short_description",
    "url_slug",
]


class TestProgramFamilyDetailView(APITestCase):
    def test_get(self):
        program_family = ProgramFamilyFactory()
        with self.login(username=self.basic_user().username):
            url = reverse(ProgramFamilyDetailView.view_name,
                          args=[program_family.id])
            response = self.client.get(url)
            assert response.data["name"] == program_family.name
            assert (response.data["short_description"] ==
                    program_family.short_description)

    def test_options(self):
        program_family = ProgramFamilyFactory()
        with self.login(username=self.basic_user().username):
            url = reverse(ProgramFamilyDetailView.view_name,
                          args=[program_family.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(PROGRAM_FAMILY_GET_FIELDS, get_options)

    def test_options_against_get(self):
        program_family = ProgramFamilyFactory()
        with self.login(username=self.basic_user().username):
            url = reverse(ProgramFamilyDetailView.view_name,
                          args=[program_family.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
