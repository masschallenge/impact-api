# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.tests.api_test_case import APITestCase
from impact.v1.metadata import (
    ORGANIZATION_ACTIONS,
    USER_ORGANIZATION_ACTIONS,
    ORGANIZATION_USER_ACTIONS,
    USER_ACTIONS
)
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
        response_json = json.loads(response.content)
        self.assertTrue(
            ORGANIZATION_ACTIONS[
                'POST'].keys() == response_json['actions']['POST'].keys()
        )

    def test_organization_users_schema_endpoint(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        response = ''
        with self.login(username=self.basic_user().username):
            url = reverse("organization_users", args=[startups[0].pk])
            response = self.client.options(url)
        response_json = json.loads(response.content)
        self.assertTrue(
            ORGANIZATION_USER_ACTIONS[
                'GET'].keys() == response_json['actions']['GET'].keys()
        )

    def test_user_organization_schema_endpoint(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        response = ''
        with self.login(username=self.basic_user().username):
            url = reverse("user_organizations", args=[startups[0].user.pk])
            response = self.client.options(url)
        response_json = json.loads(response.content)
        self.assertTrue(
            USER_ORGANIZATION_ACTIONS[
                'GET'].keys() == response_json['actions']['GET'].keys()
        )

    def test_user_schema_endpoint(self):
        count = 5
        StartupFactory.create_batch(count)
        response = ''
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.options(url)
        response_json = json.loads(response.content)
        self.assertTrue(
            USER_ACTIONS[
                'GET'].keys() == response_json['actions']['GET'].keys()
        )
