# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import reverse

from impact.tests.factories import ExpertFactory
from impact.tests.api_test_case import APITestCase

TEST_EXPERT_GROUP = "11"
TEST_INTERNAL_NOTES = "Amazing!"


class TestUserConfidentialView(APITestCase):
    def privileged_user(self):
        user = self.basic_user()
        name = settings.V1_CONFIDENTIAL_API_GROUP
        group, _ = Group.objects.get_or_create(name=name)
        user.groups.add(group)
        return user

    def test_basic_user_cannot_access(self):
        user = ExpertFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("user_confidential", args=[user.id])
            response = self.client.get(url)
            self.assertEqual(403, response.status_code)

    def test_privileged_user_can_access(self):
        user = ExpertFactory(profile__expert_group=TEST_EXPERT_GROUP,
                             profile__internal_notes=TEST_INTERNAL_NOTES)
        with self.login(username=self.privileged_user().username):
            url = reverse("user_confidential", args=[user.id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)
            self.assertEqual(TEST_EXPERT_GROUP,
                             response.data["expert_group"])
            self.assertEqual(TEST_INTERNAL_NOTES,
                             response.data["internal_notes"])
