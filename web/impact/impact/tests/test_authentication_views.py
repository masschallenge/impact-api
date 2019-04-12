# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from test_plus.test import TestCase

from impact.tests.factories import UserFactory

User = get_user_model()  # pylint: disable=invalid-name


class TestAuthenticationViews(TestCase):
    client_class = APIClient
    user_factory = UserFactory

    def test_user_login_logout(self):
        User.objects.create_user("test@testing.com", "password1!")
        self.assertTrue(User.objects.filter(email="test@testing.com").exists())
        self.get_check_200("auth_login")
        form_data = {
            "username": "test@testing.com",
            "password": "password1!",
        }
        self.post("auth_login", data=form_data)
        self.response_302()
        self.get_check_200("api-root", extra={"HTTP_ACCEPT": "text/html"})
        self.assertTemplateUsed(self.last_response, "rest_framework/api.html")
        self.assertResponseContains("test@testing.com", html=False)

        self.get("auth_logout")
        self.response_302()

        self.get(self.reverse(
            "object-list", model='startup', app='impact'))
        self.response_401()
