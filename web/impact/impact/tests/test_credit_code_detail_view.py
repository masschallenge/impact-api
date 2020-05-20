# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from .factories import RefundCodeFactory
from .api_test_case import APITestCase
from .utils import assert_fields
from ..v1.views import CreditCodeDetailView


CREDIT_CODE_GET_FIELDS = [
    "id",
    "issued_to",
    "created_at",
    "unique_code",
    "discount",
    "maximum_uses",
    "programs",
]


class TestCreditCodeDetailView(APITestCase):
    def test_get(self):
        code = RefundCodeFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(CreditCodeDetailView.view_name,
                          args=[code.pk])
            response = self.client.get(url)
            assert response.data["discount"] == code.discount
            assert response.data["issued_to"] == code.issued_to.organization.id
            assert response.data["unique_code"] == code.unique_code
            assert response.data["programs"] == [
                program.pk for program in code.programs.all()]

    def test_options(self):
        code = RefundCodeFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(CreditCodeDetailView.view_name,
                          args=[code.pk])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(CREDIT_CODE_GET_FIELDS, get_options)

    def test_options_against_get(self):
        code = RefundCodeFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(CreditCodeDetailView.view_name,
                          args=[code.pk])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
