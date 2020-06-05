# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .api_test_case import APITestCase
from .factories import OrganizationFactory


class TestOrganization(APITestCase):
    def test_str(self):
        organization = OrganizationFactory()
        assert str(organization) == organization.name
