# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.tests.factories import IndustryFactory
from impact.tests.api_test_case import APITestCase
from impact.v1.helpers import IndustryHelper


class TestIndustryListView(APITestCase):

    def test_get_industries(self):
        count = 5
        industries = IndustryFactory.create_batch(count)
        with self.login(username=self.basic_user().username):
            url = reverse("industry")
            response = self.client.get(url)
            assert response.data['count'] == count
            assert all([IndustryHelper(industry).serialize()
                        in response.data['results']
                        for industry in industries])
