# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.contexts import UserContext
from impact.tests.api_test_case import APITestCase
from django.contrib.auth import get_user_model


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

    def test_post_required_missing(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, {})
            assert response.status_code == 403

    def test_post_existing(self):
        user = UserContext().user
        data = EXAMPLE_USER.copy()
        data["email"] = user.email
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, data)
            assert response.status_code == 403
