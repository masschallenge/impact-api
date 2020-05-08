# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .tests.api_test_case import APITestCase
from .tests.factories import UserFactory
from .views import JWTCookieNameView

User = get_user_model()  # pylint: disable=invalid-name


class TestJWTCookieNameView(APITestCase):
    client_class = APIClient
    user_factory = UserFactory
    url = reverse(JWTCookieNameView.view_name)

    def test_logged_in_user_gets_response_with_cookie_name(self):
        cookie_name = 'test-jwt-name'
        with self.settings(JWT_AUTH={'JWT_AUTH_COOKIE': cookie_name}):
            with self.login(email=self.basic_user().email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)
                self.assertTrue('name' in response_data.keys())
                self.assertTrue(cookie_name in response_data['name'])

    def test_unauthenticated_user_is_denied(self):
        cookie_name = 'test-jwt-name'
        with self.settings(JWT_AUTH={'JWT_AUTH_COOKIE': cookie_name}):
            response = self.client.get(self.url)
            response_data = json.loads(response.content)
            self.assertTrue(
                response_data['detail'] == 'Authentication credentials '
                                           'were not provided.')
