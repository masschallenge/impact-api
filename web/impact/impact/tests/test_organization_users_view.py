# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    PartnerTeamMemberFactory,
    StartupTeamMemberFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields

ORGANIZATION_USERS_GET_FIELDS = ["users"]


class TestOrganizationUsersView(APITestCase):

    def test_get(self):
        startup_team_member = StartupTeamMemberFactory(
            startup_administrator=True)
        startup_user_id = startup_team_member.user.id
        partner_team_member = PartnerTeamMemberFactory(
            partner__organization=startup_team_member.startup.organization)
        partner_user_id = partner_team_member.team_member.id
        with self.login(username=self.basic_user().username):
            url = reverse("organization_users",
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
        startup = StartupTeamMemberFactory(startup_administrator=True).startup
        with self.login(username=self.basic_user().username):
            url = reverse("organization_users", args=[startup.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(ORGANIZATION_USERS_GET_FIELDS, get_options)
