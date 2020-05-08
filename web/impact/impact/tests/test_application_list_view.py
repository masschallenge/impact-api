import json
from jsonschema import Draft4Validator

from django.urls import reverse
from .tests.factories import ApplicationFactory
from .tests.api_test_case import APITestCase
from .tests.utils import assert_fields
from .v1.views import ApplicationListView

from .tests.test_application_detail_view import (
    APPLICATION_GET_FIELDS,
)


class TestApplicationListView(APITestCase):
    url = reverse(ApplicationListView.view_name)

    def test_get(self):
        count = 5
        applications = ApplicationFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data["count"] == count
            assert all([ApplicationListView.serialize(application)
                        in response.data["results"]
                        for application in applications])

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(APPLICATION_GET_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):

            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
