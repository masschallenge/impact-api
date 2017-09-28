# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    IndustryFactory,
    OrganizationFactory,
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
            assert (response.data["public_inquiry_email"] ==
                    startup.public_inquiry_email)
            assert response.data["is_startup"] is True
            assert response.data["is_partner"] is False

    def test_get_startup_with_industries(self):
        primary_industry = IndustryFactory()
        additional_industries = IndustryFactory.create_batch(2)
        startup = StartupFactory(
            primary_industry=primary_industry,
            additional_industries=additional_industries)
        with self.login(username=self.basic_user().username):
            url = reverse("organization_detail",
                          args=[startup.organization.id])
            response = self.client.get(url)
            assert response.data["primary_industry_id"] == primary_industry.id
            assert all([industry.id in response.data["additional_industry_ids"]
                        for industry in additional_industries])

    def test_get_partner(self):
        partner = PartnerFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_detail",
                          args=[partner.organization.id])
            response = self.client.get(url)
            assert response.data["name"] == partner.organization.name
            assert response.data["url_slug"] == partner.organization.url_slug
            assert (response.data["public_inquiry_email"] ==
                    partner.public_inquiry_email)
            assert response.data["is_startup"] is False
            assert response.data["is_partner"] is True

    def test_get_org_is_both_partner_and_startup(self):
        partner = PartnerFactory()

        with self.login(username=self.basic_user().username):
            url = reverse("organization_detail",
                          args=[partner.organization.id])
            response = self.client.get(url)
            assert response.data["name"] == partner.organization.name
            assert response.data["url_slug"] == partner.organization.url_slug
            assert (response.data["public_inquiry_email"] ==
                    partner.public_inquiry_email)
            assert response.data["is_startup"] is False
            assert response.data["is_partner"] is True

    def test_organization_has_no_startup_nor_partner(self):
        organization = OrganizationFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_detail",
                          args=[organization.id])
            response = self.client.get(url)
            assert response.data["name"] == organization.name
            assert response.data["url_slug"] == organization.url_slug
            assert (response.data["public_inquiry_email"] ==
                    organization.public_inquiry_email)
            assert response.data["is_startup"] is False
            assert response.data["is_partner"] is False
