# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from .tests.factories import (
    PartnerTeamMemberFactory,
    StartupTeamMemberFactory,
)

from .tests.api_test_case import APITestCase
from .tests.utils import assert_fields
from .v1.views.organization_users_view import (
    ORGANIZATION_USER_FIELDS,
    OrganizationUsersView,
)

ORGANIZATION_USERS_GET_FIELDS = ["users"]


class TestOrganizationUsersView(APITestCase):

    def test_get(self):
        startup_team_member = StartupTeamMemberFactory(
            startup_administrator=True)
        startup_user_id = startup_team_member.user.id
        partner_team_member = PartnerTeamMemberFactory(
            partner__organization=startup_team_member.startup.organization)
        partner_user_id = partner_team_member.team_member.id
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationUsersView.view_name,
                          args=[startup_team_member.startup.organization.id])
            response = self.client.get(url)
            users = response.data["users"]
            self.assertEqual(len(users), 2)
            startup_user = [user for user in users
                            if user["id"] == startup_user_id][0]
            self.assertTrue(startup_user["startup_administrator"])
            self.assertFalse(startup_user["primary_contact"])
            partner_user = [user for user in users
                            if user["id"] == partner_user_id][0]
            self.assertFalse(partner_user["partner_administrator"])

    def test_options(self):
        stm = StartupTeamMemberFactory(startup_administrator=True)
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationUsersView.view_name,
                          args=[stm.startup.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(ORGANIZATION_USERS_GET_FIELDS, get_options)
            assert (ORGANIZATION_USER_FIELDS.keys() ==
                    get_options["users"]["item"]["properties"].keys())

    def test_options_against_get(self):
        stm = StartupTeamMemberFactory(startup_administrator=True)
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationUsersView.view_name,
                          args=[stm.startup.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
