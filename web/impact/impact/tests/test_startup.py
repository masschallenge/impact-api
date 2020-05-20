# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .api_test_case import APITestCase
from .factories import StartupFactory


class TestStartup(APITestCase):
    def test_str(self):
        startup = StartupFactory()
        assert str(startup) == startup.name
