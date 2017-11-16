# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.tests.api_test_case import APITestCase
from impact.tests.factories import ProgramFactory


class TestProgram(APITestCase):
    def test_str(self):
        program = ProgramFactory()
        assert str(program) == program.name
