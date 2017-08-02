# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    OrganizationFactory,
    PartnerTeamMemberFactory,
    StartupTeamMemberFactory,
)

from impact.tests.api_test_case import APITestCase


class TestOrganizationUsersView(APITestCase):

    def test_get(self):
        startup_team_member = StartupTeamMemberFactory()
        partner_team_member = PartnerTeamMemberFactory(
            partner__organization=startup_team_member.startup.organization)
        with self.login(username=self.basic_user().username):
            url = reverse("organization_users",
                          args=[startup_team_member.startup.organization.id])
            response = self.client.get(url)
            assert startup_team_member.user_id in response.data['users']
            assert partner_team_member.team_member_id in response.data['users']
