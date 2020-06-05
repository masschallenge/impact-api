# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse
from .factories import RefundCodeFactory
from .api_test_case import APITestCase
from .test_credit_code_detail_view import (
    CREDIT_CODE_GET_FIELDS,
)
from .utils import assert_fields
from ..v1.views import CreditCodeListView


class TestCreditCodeListView(APITestCase):
    url = reverse(CreditCodeListView.view_name)

    def test_get(self):
        count = 5
        codes = RefundCodeFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data["count"] == count
            assert all([CreditCodeListView.serialize(code)
                        in response.data["results"]
                        for code in codes])

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(CREDIT_CODE_GET_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):

            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
