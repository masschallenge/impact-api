from impact.tests.api_test_case import APITestCase
from impact.tests.factories import CriterionOptionSpecFactory
from impact.v1.helpers import CriterionHelper

class TestCriterionHelper(APITestCase):
    def test_find_helper_caches_by_criterion(self):
        
        criterion = CriterionOptionSpecFactory().criterion
        helper_instance = CriterionHelper.find_helper(criterion)
        assert CriterionHelper.find_helper(criterion) == helper_instance
