# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse
from impact.tests.factories import JudgingRoundFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.test_judging_round_detail_view import (
    JUDGING_ROUND_GET_FIELDS,
)
from impact.tests.utils import assert_fields
from impact.v1.views import JudgingRoundListView


class TestJudgingRoundListView(APITestCase):
    url = reverse(JudgingRoundListView.view_name)

    def test_get(self):
        count = 5
        program_families = JudgingRoundFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data["count"] == count
            assert all([JudgingRoundListView.serialize(judging_round)
                        in response.data["results"]
                        for judging_round in program_families])

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(JUDGING_ROUND_GET_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):

            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
