# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import IndustryFactory
from impact.tests.api_test_case import APITestCase


class TestIndustryDetailView(APITestCase):
    def test_get_industry(self):
        industry = IndustryFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("industry_detail", args=[industry.id])
            response = self.client.get(url)
            assert response.data["name"] == industry.name
            assert "parent_id" not in response.data
            assert response.data["full_name"] == str(industry)

    def test_get_industry_with_parent(self):
        parent = IndustryFactory()
        industry = IndustryFactory(parent=parent)
        with self.login(username=self.basic_user().username):
            url = reverse("industry_detail", args=[industry.id])
            response = self.client.get(url)
            assert response.data["name"] == industry.name
            assert response.data["parent_id"] == industry.parent_id
            assert response.data["full_name"] == str(industry)
