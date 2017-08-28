from impact.tests.api_test_case import APITestCase
from impact.tests.factories import ScenarioFactory


class TestScenario(APITestCase):
    def test_str(self):
        scenario = ScenarioFactory()
        assert str(scenario) == scenario.name
