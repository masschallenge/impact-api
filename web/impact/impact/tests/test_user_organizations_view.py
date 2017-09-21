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
        startup_team_member = StartupTeamMemberFactory(
            startup_administrator=True)
        startup_org_id = startup_team_member.startup.organization_id
        partner_team_member = PartnerTeamMemberFactory(
            team_member=startup_team_member.user)
        partner_org_id = partner_team_member.partner.organization_id
        with self.login(username=self.basic_user().username):
            url = reverse("user_organizations",
                          args=[startup_team_member.user_id])
            response = self.client.get(url)
            startups = [org for org in response.data["organizations"]
                        if org["id"] == startup_org_id]
            self.assertEqual(len(startups), 1)
            self.assertEqual(startups[0]["startup_administrator"], True)
            self.assertEqual(startups[0]["primary_contact"], False)
            partners = [org for org in response.data["organizations"]
                        if org["id"] == partner_org_id]
            self.assertEqual(len(partners), 1)
            self.assertEqual(partners[0]["partner_administrator"], False)
