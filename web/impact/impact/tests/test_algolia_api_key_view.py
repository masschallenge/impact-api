# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from impact.tests.api_test_case import APITestCase
from impact.views import AlgoliaApiKeyView
from impact.tests.factories import UserFactory
from django.urls import reverse
import simplejson as json

User = get_user_model()  # pylint: disable=invalid-name


class TestAlgoliaApiKeyView(APITestCase):
    client_class = APIClient
    user_factory = UserFactory
    url = reverse(AlgoliaApiKeyView.view_name)

    def test_logged_in_user_generates_token(self):
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=self.basic_user().email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)
                self.assertTrue('token' in response_data.keys())

    def test_unauthenticated_user_is_denied(self):
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            response = self.client.get(self.url)
            response_data = json.loads(response.content)
            self.assertTrue(
                response_data['detail'] == 'Authentication credentials '
                                           'were not provided.')
