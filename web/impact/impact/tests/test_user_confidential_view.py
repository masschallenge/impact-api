# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import reverse

from .factories import ExpertFactory
from .api_test_case import APITestCase
from .utils import assert_fields
from ..v1.views.user_confidential_view import UserConfidentialView

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
        with self.login(email=self.basic_user().email):
            url = reverse(UserConfidentialView.view_name, args=[user.id])
            response = self.client.get(url)
            self.assertEqual(403, response.status_code)

    def test_privileged_user_can_access(self):
        user = ExpertFactory(profile__expert_group=TEST_EXPERT_GROUP,
                             profile__internal_notes=TEST_INTERNAL_NOTES)
        with self.login(email=self.privileged_user().email):
            url = reverse(UserConfidentialView.view_name, args=[user.id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)
            self.assertEqual(TEST_EXPERT_GROUP,
                             response.data["expert_group"])
            self.assertEqual(TEST_INTERNAL_NOTES,
                             response.data["internal_notes"])

    def test_options(self):
        user = ExpertFactory(profile__expert_group=TEST_EXPERT_GROUP,
                             profile__internal_notes=TEST_INTERNAL_NOTES)
        with self.login(email=self.privileged_user().email):
            url = reverse(UserConfidentialView.view_name, args=[user.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_data = response.data["actions"]["GET"]
            assert get_data["type"] == "object"
            get_options = get_data["properties"]
            assert_fields(UserConfidentialView.fields().keys(), get_options)

    def test_options_against_get(self):
        user = ExpertFactory(profile__expert_group=TEST_EXPERT_GROUP,
                             profile__internal_notes=TEST_INTERNAL_NOTES)
        with self.login(email=self.privileged_user().email):
            url = reverse(UserConfidentialView.view_name, args=[user.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
