# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    PartnerFactory,
    StartupFactory,
)

from impact.tests.api_test_case import APITestCase


class TestOrganizationDetailView(APITestCase):

    def test_get_startup(self):
        startup = StartupFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_detail",
                          args=[startup.organization.id])
            response = self.client.get(url)
            assert response.data["name"] == startup.organization.name
            assert response.data["url_slug"] == startup.organization.url_slug
            assert response.data["is_startup"] is True
            assert response.data["is_partner"] is False

    def test_get_partner(self):
        partner = PartnerFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_detail",
                          args=[partner.organization.id])
            response = self.client.get(url)
            assert response.data["name"] == partner.organization.name
            assert response.data["url_slug"] == partner.organization.url_slug
            assert response.data["is_startup"] is False
            assert response.data["is_partner"] is True
