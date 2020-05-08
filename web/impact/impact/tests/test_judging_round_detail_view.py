# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from .tests.factories import JudgingRoundFactory
from .tests.api_test_case import APITestCase
from .tests.utils import assert_fields
from .v1.views import JudgingRoundDetailView

JUDGING_ROUND_GET_FIELDS = [
    "id",
    "name",
    "program_id",
    "cycle_id",
    "cycle_based_round",
    "round_type",
]


class TestJudgingRoundDetailView(APITestCase):
    def test_get(self):
        judging_round = JudgingRoundFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(JudgingRoundDetailView.view_name,
                          args=[judging_round.id])
            response = self.client.get(url)
            assert response.data["name"] == judging_round.name
            assert (response.data["program_id"] ==
                    judging_round.program_id)

    def test_options(self):
        judging_round = JudgingRoundFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(JudgingRoundDetailView.view_name,
                          args=[judging_round.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(JUDGING_ROUND_GET_FIELDS, get_options)

    def test_options_against_get(self):
        judging_round = JudgingRoundFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(JudgingRoundDetailView.view_name,
                          args=[judging_round.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))

    def test_staff_user_can_view(self):
        judging_round = JudgingRoundFactory()
        email = self.staff_user().email
        with self.login(email=email):
            url = reverse(JudgingRoundDetailView.view_name,
                          args=[judging_round.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["name"], judging_round.name)
            self.assertEqual(response.data["program_id"],
                             judging_round.program_id)
