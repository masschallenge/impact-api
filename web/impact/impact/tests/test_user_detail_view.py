# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.contexts import UserContext
from impact.tests.api_test_case import APITestCase


class TestUserDetailView(APITestCase):

    def test_get(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            response = self.client.get(url)
            assert user.full_name == response.data["first_name"]
            assert user.short_name == response.data["last_name"]
            assert user.last_login == response.data["last_login"]

    def test_patch(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            is_active = not user.is_active
            first_name = "David"
            data = {
                "is_active": is_active,
                "first_name": first_name,
                "gender": "Male",
                }
            self.client.patch(url, data)
            user.refresh_from_db()
            assert user.is_active == is_active
            assert user.full_name == first_name

    def test_patch_invalid_key(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_key = "bad key"
            response = self.client.patch(url, {bad_key: True})
            assert response.status_code == 403
            assert bad_key in response.data

    def test_patch_invalid_gender(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_gender = "bad gender"
            response = self.client.patch(url, {"gender": bad_gender})
            assert response.status_code == 403
            assert bad_gender in response.data
