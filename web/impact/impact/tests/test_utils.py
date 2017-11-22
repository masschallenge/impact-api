# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models.utils import (
    model_name_to_snake,
    snake_to_model_name,
)
from impact.tests.api_test_case import APITestCase


empty_string = ''
CAMEL_CASE_MODEL_NAME = 'ProgramStartupStatus'
LOWER_CASE_MODEL_NAME = 'programstartupstatus'
SNAKE_CASE_MODEL_NAME = 'program_startup_status'


class TestUtils(APITestCase):
    def test_empty_string_snake_case_returns_nothing(self):
        assert model_name_to_snake(empty_string) == ''

    def test_model_name_to_snake_case(self):
        assert model_name_to_snake(
            CAMEL_CASE_MODEL_NAME) == SNAKE_CASE_MODEL_NAME

    def test_lowercase_model_name_not_snaked(self):
        assert model_name_to_snake(
            LOWER_CASE_MODEL_NAME) == LOWER_CASE_MODEL_NAME

    def test_snake_case_to_model_name(self):
        assert snake_to_model_name(
            SNAKE_CASE_MODEL_NAME) == CAMEL_CASE_MODEL_NAME
