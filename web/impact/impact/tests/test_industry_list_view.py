# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse
from impact.tests.factories import IndustryFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.helpers import MPTT_FIELDS
from impact.v1.views import IndustryListView


class TestIndustryListView(APITestCase):
    url = reverse(IndustryListView.view_name)

    def test_get_industries(self):
        count = 5
        industries = IndustryFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data['count'] == count
            assert all([IndustryListView.serialize(industry)
                        in response.data['results']
                        for industry in industries])

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(MPTT_FIELDS.keys(), get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):
            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
