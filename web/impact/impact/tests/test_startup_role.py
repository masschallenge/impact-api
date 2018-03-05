# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.tests.api_test_case import APITestCase
from impact.tests.factories import StartupRoleFactory


class TestStartupRole(APITestCase):
    def test_str(self):
        role = StartupRoleFactory()
        assert str(role) == role.name
