# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .tests.api_test_case import APITestCase
from .tests.factories import BaseProfileFactory


class TestBaseProfile(APITestCase):
    def test_str(self):
        base_profile = BaseProfileFactory()
        bp_string = str(base_profile)
        assert base_profile.user.first_name in bp_string
        assert base_profile.user.last_name in bp_string

    def test_str_with_partial_name(self):
        base_profile = BaseProfileFactory(user__first_name="")
        bp_string = str(base_profile)
        assert base_profile.user.last_name not in bp_string
        assert base_profile.user.email in bp_string
