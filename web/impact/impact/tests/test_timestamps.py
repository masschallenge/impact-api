# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from impact.tests.factories import (
    CurrencyFactory,
    FunctionalExpertiseFactory,
    IndustryFactory,
    StartupProgramInterestFactory,
)


class TestTimestamps(TestCase):
    def test_currency(self):
        currency = CurrencyFactory()
        assert currency.created_at <= currency.updated_at

    def test_non_mc_models(self):
        for factory in [FunctionalExpertiseFactory,
                        IndustryFactory,
                        StartupProgramInterestFactory]:
            obj = factory()
            with self.assertRaises(AttributeError):
                assert obj.created_at <= obj.updated_at
