# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from impact.tests.factories import ReferenceFactory


class TestReference(TestCase):

    def test_submitted_str(self):
        assert "request" not in str(ReferenceFactory())

    def test_unsubmitted_str(self):
        assert "request" in str(ReferenceFactory(submitted=None))
