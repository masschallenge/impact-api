# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .tests.api_test_case import APITestCase
from .tests.factories import ProgramCycleFactory


class TestProgramCycle(APITestCase):
    def test_str(self):
        cycle = ProgramCycleFactory()
        assert str(cycle) == cycle.name
