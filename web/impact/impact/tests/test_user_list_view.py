# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from django.contrib.auth import get_user_model

from impact.tests.contexts import UserContext
from impact.tests.api_test_case import APITestCase
from impact.v1.views.user_list_view import EMAIL_EXISTS_ERROR


EXAMPLE_USER = {
    "first_name": "First",
    "last_name": "Last",
    "email": "test@example.com",
    "gender": "o",
}
User = get_user_model()


class TestUserListView(APITestCase):

    def test_get(self):
        user1 = UserContext().user
        user2 = UserContext().user
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.get(url)
            emails = [result["email"] for result in response.data["results"]]
            assert user1.email in emails
            assert user2.email in emails

    def test_post(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, EXAMPLE_USER)
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_USER["email"]

    def test_post_without_required_field(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, {})
            assert response.status_code == 403

    def test_post_bad_key(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            bad_key = "bad key"
            response = self.client.post(url, {bad_key: True})
            assert response.status_code == 403
            assert any([bad_key in error for error in response.data])

    def test_post_with_existing_email(self):
        user = UserContext().user
        data = EXAMPLE_USER.copy()
        data["email"] = user.email
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, data)
            assert response.status_code == 403
            assert EMAIL_EXISTS_ERROR.format(user.email) in response.data
