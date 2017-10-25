# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.tests.api_test_case import APITestCase
from impact.v1.helpers import (
    ORGANIZATION_FIELDS,
    USER_FIELDS,
)
from impact.v1.helpers import ORGANIZATION_USER_FIELDS
from impact.tests.factories import (
    StartupFactory
)
import simplejson as json


class TestSchemaEndpoints(APITestCase):
    def test_organization_schema_endpoint(self):
        count = 5
        StartupFactory.create_batch(count)
        response = ''
        with self.login(username=self.basic_user().username):
            url = reverse("organization")
            response = self.client.options(url)
        results = response.data["actions"]["GET"]["properties"]["results"]
        properties = results["item"]["properties"]
        self.assertEqual(ORGANIZATION_FIELDS.keys(), properties.keys())

    def test_organization_users_schema_endpoint(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        response = ''
        with self.login(username=self.basic_user().username):
            url = reverse("organization_users", args=[startups[0].pk])
            response = self.client.options(url)
        response_json = json.loads(response.content, encoding='utf8')
        self.assertEqual(
            ORGANIZATION_USER_FIELDS.keys(),
            response_json["actions"]["GET"]["properties"]["users"]["item"][
                "properties"].keys())

    def test_user_organization_schema_endpoint(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        response = ''
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.options(url)
        results = response.data["actions"]["GET"]["properties"]["results"]
        properties = results["item"]["properties"]
        self.assertEqual(USER_FIELDS.keys(), properties.keys())
