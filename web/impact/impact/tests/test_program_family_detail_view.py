# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import ProgramFamilyFactory
from impact.tests.api_test_case import APITestCase


class TestProgramFamilyDetailView(APITestCase):
    def test_get(self):
        program_family = ProgramFamilyFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("program_family_detail", args=[program_family.id])
            response = self.client.get(url)
            assert response.data["name"] == program_family.name
            assert (response.data["short_description"] ==
                    program_family.short_description)
