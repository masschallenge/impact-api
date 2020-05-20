# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator
from django.urls import reverse

from .factories import IndustryFactory
from .api_test_case import APITestCase
from .utils import assert_fields
from .v1.helpers import MPTT_FIELDS
from .v1.views import IndustryDetailView


class TestIndustryDetailView(APITestCase):
    def test_get_industry(self):
        industry = IndustryFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(IndustryDetailView.view_name, args=[industry.id])
            response = self.client.get(url)
            assert response.data["name"] == industry.name
            assert "parent_id" not in response.data
            assert response.data["full_name"] == str(industry)

    def test_get_industry_with_parent(self):
        parent = IndustryFactory()
        industry = IndustryFactory(parent=parent)
        with self.login(email=self.basic_user().email):
            url = reverse(IndustryDetailView.view_name, args=[industry.id])
            response = self.client.get(url)
            assert response.data["name"] == industry.name
            assert response.data["parent_id"] == industry.parent_id
            assert response.data["full_name"] == str(industry)

    def test_options(self):
        industry = IndustryFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(IndustryDetailView.view_name, args=[industry.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(MPTT_FIELDS.keys(), get_options)

    def test_options_against_get(self):
        industry = IndustryFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(IndustryDetailView.view_name, args=[industry.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
