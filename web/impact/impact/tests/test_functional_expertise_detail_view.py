# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator
from django.urls import reverse

from impact.tests.factories import FunctionalExpertiseFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.views import FunctionalExpertiseDetailView

FUNCTIONAL_EXPERTISE_GET_FIELDS = [
    "id",
    "name",
    "full_name",
    "parent_id",
]


class TestFunctionalExpertiseDetailView(APITestCase):
    def test_get_functional_expertise(self):
        functional_expertise = FunctionalExpertiseFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(FunctionalExpertiseDetailView.view_name,
                          args=[functional_expertise.id])
            response = self.client.get(url)
            assert response.data["name"] == functional_expertise.name
            assert "parent_id" not in response.data
            assert response.data["full_name"] == str(functional_expertise)

    def test_get_functional_expertise_with_parent(self):
        parent = FunctionalExpertiseFactory()
        functional_expertise = FunctionalExpertiseFactory(parent=parent)
        with self.login(email=self.basic_user().email):
            url = reverse(FunctionalExpertiseDetailView.view_name,
                          args=[functional_expertise.id])
            response = self.client.get(url)
            assert response.data["name"] == functional_expertise.name
            assert response.data["parent_id"] == functional_expertise.parent_id
            assert response.data["full_name"] == str(functional_expertise)

    def test_options(self):
        functional_expertise = FunctionalExpertiseFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(FunctionalExpertiseDetailView.view_name,
                          args=[functional_expertise.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(FUNCTIONAL_EXPERTISE_GET_FIELDS, get_options)

    def test_options_against_get(self):
        functional_expertise = FunctionalExpertiseFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(FunctionalExpertiseDetailView.view_name,
                          args=[functional_expertise.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
