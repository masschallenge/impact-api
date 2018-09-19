# MIT License
# Copyright (c) 2018 MassChallenge, Inc.

from accelerator.models import (
    Clearance,
    CLEARANCE_LEVEL_POM,
    CLEARANCE_LEVEL_GLOBAL_MANAGER
)
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import ClearanceFactory


class TestClearanceOrdering(APITestCase):

    def test_higher_clearance_accepted(self):
        clearance = ClearanceFactory(level=CLEARANCE_LEVEL_GLOBAL_MANAGER)
        user = clearance.user
        cleared = Clearance.objects.check_clearance(user, CLEARANCE_LEVEL_POM)
        self.assertTrue(cleared)

    def test_equal_clearance_accepted(self):
        clearance = ClearanceFactory(level=CLEARANCE_LEVEL_GLOBAL_MANAGER)
        user = clearance.user
        cleared = Clearance.objects.check_clearance(
            user, CLEARANCE_LEVEL_GLOBAL_MANAGER)
        self.assertTrue(cleared)

    def test_lower_clearance_rejected(self):
        clearance = ClearanceFactory(level=CLEARANCE_LEVEL_POM)
        user = clearance.user
        cleared = Clearance.objects.check_clearance(
            user, CLEARANCE_LEVEL_GLOBAL_MANAGER)
        self.assertFalse(cleared)
