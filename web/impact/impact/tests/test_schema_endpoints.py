# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from .tests.api_test_case import APITestCase
from .v1.helpers import (
    ORGANIZATION_FIELDS,
    USER_FIELDS,
)
from .v1.helpers import ORGANIZATION_USER_FIELDS
from .tests.factories import (
    StartupFactory
)
import json


class TestSchemaEndpoints(APITestCase):
    def test_organization_schema_endpoint(self):
        count = 5
        StartupFactory.create_batch(count)
        response = ''
        with self.login(email=self.basic_user().email):
            url = reverse("organization")
            response = self.client.options(url)
        results = response.data["actions"]["GET"]["properties"]["results"]
        properties = results["item"]["properties"]
        self.assertEqual(ORGANIZATION_FIELDS.keys(), properties.keys())

    def test_organization_users_schema_endpoint(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        response = ''
        with self.login(email=self.basic_user().email):
            url = reverse("organization_users", args=[startups[0].pk])
            response = self.client.options(url)
        response_json = json.loads(response.content)
        self.assertEqual(
            ORGANIZATION_USER_FIELDS.keys(),
            response_json["actions"]["GET"]["properties"]["users"]["item"][
                "properties"].keys())

    def test_user_organization_schema_endpoint(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        response = ''
        with self.login(email=self.basic_user().email):
            url = reverse("user_organizations", args=[startups[0].user.pk])
            response = self.client.options(url)
        response_json = json.loads(response.content)
        self.assertEqual(
            ORGANIZATION_USER_FIELDS.keys(),
            response_json["actions"]["GET"]["properties"]["organizations"][
                "item"]["properties"].keys())

    def test_user_schema_endpoint(self):
        count = 5
        StartupFactory.create_batch(count)
        response = ''
        with self.login(email=self.basic_user().email):
            url = reverse("user")
            response = self.client.options(url)
        results = response.data["actions"]["GET"]["properties"]["results"]
        properties = results["item"]["properties"]
        response_keys = set(properties.keys())
        self.assertTrue(len(response_keys) > 0)
        self.assertFalse(response_keys - set(USER_FIELDS.keys()))
