# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from impact.tests.factories import ProgramCycleFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.views import ProgramCycleDetailView

PROGRAM_CYCLE_GET_FIELDS = [
    "id",
    "name",
    "short_name",
    "applications_open",
    "application_open_date",
    "application_early_deadline_date",
    "application_final_deadline_date",
    "advertised_final_deadline",
]


class TestProgramCycleDetailView(APITestCase):
    def test_get(self):
        program_cycle = ProgramCycleFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ProgramCycleDetailView.view_name,
                          args=[program_cycle.id])
            response = self.client.get(url)
            assert response.data["name"] == program_cycle.name
            assert (response.data["applications_open"] ==
                    program_cycle.applications_open)

    def test_options(self):
        program_cycle = ProgramCycleFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ProgramCycleDetailView.view_name,
                          args=[program_cycle.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(PROGRAM_CYCLE_GET_FIELDS, get_options)

    def test_options_against_get(self):
        program_cycle = ProgramCycleFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ProgramCycleDetailView.view_name,
                          args=[program_cycle.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
