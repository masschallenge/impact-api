# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    PartnerFactory,
    StartupFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.v1.views.organization_list_view import serialize_org


class TestOrganizationDetailView(APITestCase):

    def test_get_startup(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        with self.login(username=self.basic_user().username):
            url = reverse("organization")
            response = self.client.get(url)
            assert response.data['count'] == count
            assert all([serialize_org(startup.organization)
                        in response.data['results']
                        for startup in startups])

    def test_get_partner(self):
        count = 5
        partners = PartnerFactory.create_batch(5)
        with self.login(username=self.basic_user().username):
            url = reverse("organization")
            response = self.client.get(url)
            assert response.data['count'] == count
            assert all([serialize_org(partner.organization)
                        in response.data['results']
                        for partner in partners])
