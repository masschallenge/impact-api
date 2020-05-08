# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .tests.api_test_case import APITestCase
from .tests.factories import ScenarioFactory


class TestScenario(APITestCase):
    def test_str(self):
        scenario = ScenarioFactory()
        assert str(scenario) == scenario.name
