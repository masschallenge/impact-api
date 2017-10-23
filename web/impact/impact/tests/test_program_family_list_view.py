# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.tests.factories import ProgramFamilyFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.test_program_family_detail_view import (
    PROGRAM_FAMILY_GET_FIELDS,
)
from impact.tests.utils import assert_fields
from impact.v1.helpers import ProgramFamilyHelper


class TestProgramFamilyListView(APITestCase):
    def test_get(self):
        count = 5
        program_families = ProgramFamilyFactory.create_batch(count)
        with self.login(username=self.basic_user().username):
            url = reverse("program_family")
            response = self.client.get(url)
            assert response.data["count"] == count
            assert all([ProgramFamilyHelper(program_family).serialize()
                        in response.data["results"]
                        for program_family in program_families])

    def test_options(self):
        with self.login(username=self.basic_user().username):
            url = reverse("program_family")
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["item"]["properties"]
            assert_fields(PROGRAM_FAMILY_GET_FIELDS, get_options)
