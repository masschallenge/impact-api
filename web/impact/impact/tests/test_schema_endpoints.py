# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.tests.api_test_case import APITestCase
from impact.v1.helpers import USER_FIELDS
from impact.v1.views.organization_detail_view import OrganizationDetailView
from impact.v1.views.organization_users_view import OrganizationUsersView
from impact.v1.views.user_organizations_view import UserOrganizationsView
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
            OrganizationDetailView.METADATA_ACTIONS[
                'GET'].keys() == response_json['actions']['GET'].keys()
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
            OrganizationUsersView.METADATA_ACTIONS[
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
            UserOrganizationsView.METADATA_ACTIONS[
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
        properties = response_json["actions"]["GET"]["item"]["properties"]
        self.assertEqual(USER_FIELDS.keys(), properties.keys())
