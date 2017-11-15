from impact.tests.api_test_case import APITestCase
from impact.models.utils import (
    camel_case_to_snake,
    snake_to_camel_case,
)

camel_case = 'ProgramStartupStatus'
snake_case = 'program_startup_status'


class TestSnakeAndCamelCasing(APITestCase):
    def test_camel_case_to_snake_case(self):
        assert camel_case_to_snake(camel_case) == snake_case

    def test_snake_case_to_camel_case(self):
        assert snake_to_camel_case(snake_case) == camel_case
