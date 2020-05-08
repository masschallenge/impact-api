# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse
from .tests.factories import ApplicationFactory
from .tests.api_test_case import APITestCase
from .tests.utils import assert_fields
from .v1.views import ApplicationDetailView

APPLICATION_GET_FIELDS = [
    "id",
    "created_at",
    "updated_at",
    "application_status",
    "cycle",
    "startup",
    "application_type",
]


class TestApplicationDetailView(APITestCase):
    def test_get(self):
        application = ApplicationFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ApplicationDetailView.view_name,
                          args=[application.id])
            response = self.client.get(url)
            assert response.data["created_at"] == application.created_at
            assert response.data["updated_at"] == application.updated_at
            assert (response.data["application_status"] ==
                    application.application_status)
            assert response.data["cycle"] == application.cycle.id
            assert response.data["startup"] == application.startup.id
            assert (response.data["application_type"] ==
                    application.application_type.id)

    def test_options(self):
        application = ApplicationFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ApplicationDetailView.view_name,
                          args=[application.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(APPLICATION_GET_FIELDS, get_options)

    def test_options_against_get(self):
        application = ApplicationFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(ApplicationDetailView.view_name,
                          args=[application.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
