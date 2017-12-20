# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse
from impact.tests.factories import FunctionalExpertiseFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.test_functional_expertise_detail_view import (
    FUNCTIONAL_EXPERTISE_GET_FIELDS
)
from impact.tests.utils import assert_fields
from impact.v1.views import FunctionalExpertiseListView


class TestFunctionalExpertiseListView(APITestCase):
    url = reverse(FunctionalExpertiseListView.view_name)

    def test_get_functional_expertise(self):
        count = 5
        functional_expertise = FunctionalExpertiseFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data['count'] == count
            assert all([FunctionalExpertiseListView.serialize(expertise)
                        in response.data['results']
                        for expertise in functional_expertise])

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(FUNCTIONAL_EXPERTISE_GET_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):
            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
