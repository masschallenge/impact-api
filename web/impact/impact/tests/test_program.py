# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .tests.api_test_case import APITestCase
from .tests.factories import ProgramFactory


class TestProgram(APITestCase):
    def test_str(self):
        program = ProgramFactory()
        assert str(program) == program.name
