# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    PartnerTeamMemberFactory,
    StartupTeamMemberFactory,
)

from impact.tests.api_test_case import APITestCase


class TestUserOrganizationsView(APITestCase):

    def test_get(self):
        startup_team_member = StartupTeamMemberFactory()
        partner_team_member = PartnerTeamMemberFactory(
            team_member=startup_team_member.user)
        with self.login(username=self.basic_user().username):
            url = reverse("user_organizations",
                          args=[startup_team_member.user_id])
            response = self.client.get(url)
            assert startup_team_member.startup_id in response.data[
                'organizations']
            assert partner_team_member.partner_id in response.data[
                'organizations']
