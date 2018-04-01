# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from impact.tests.factories import (
    FunctionalExpertiseFactory,
    IndustryFactory,
    StartupProgramInterestFactory,
    StartupFactory,
)


class TestTimestamps(TestCase):
    def test_startup(self):
        startup = StartupFactory()
        assert startup.created_at <= startup.updated_at

    def test_non_mc_models(self):
        for factory in [FunctionalExpertiseFactory,
                        IndustryFactory,
                        StartupProgramInterestFactory]:
            obj = factory()
            assert obj.created_at <= obj.updated_at
