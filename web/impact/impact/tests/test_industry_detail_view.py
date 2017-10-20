# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import IndustryFactory
from impact.tests.api_test_case import APITestCase
INDUSTRY_GET_FIELDS = [
    "id",
    "name",
    "full_name",
    "parent_id",
]
from impact.tests.utils import assert_fields


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

    def test_options(self):
        industry = IndustryFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("industry_detail", args=[industry.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(INDUSTRY_GET_FIELDS, get_options)
