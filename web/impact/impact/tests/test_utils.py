# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models.utils import (
    model_name_to_snake,
    snake_to_model_name,
)
from impact.tests.api_test_case import APITestCase


empty_string = ''
model_name = 'ProgramStartupStatus'
lowercase_model_name = 'programstartupstatus'
snake_case = 'program_startup_status'


class TestUtils(APITestCase):
    def test_empty_string_snake_case_returns_nothing(self):
        assert model_name_to_snake(empty_string) == ''

    def test_model_name_to_snake_case(self):
        assert model_name_to_snake(model_name) == snake_case

    def test_lowercase_model_name_not_snaked(self):
        assert model_name_to_snake(lowercase_model_name) != snake_case

    def test_snake_case_to_model_name(self):
        assert snake_to_model_name(snake_case) == model_name
