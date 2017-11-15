from impact.tests.api_test_case import APITestCase
from impact.tests.factories import ProgramCycleFactory


class TestProgramCycle(APITestCase):
    def test_str(self):
        cycle = ProgramCycleFactory()
        assert str(cycle) == cycle.name
