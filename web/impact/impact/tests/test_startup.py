from impact.tests.api_test_case import APITestCase
from impact.tests.factories import StartupFactory


class TestStartup(APITestCase):
    def test_str(self):
        startup = StartupFactory()
        assert str(startup) == startup.name
