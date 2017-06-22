# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from impact.utils import get_profile
from impact.tests.contexts import (
    UserContext,
)
from impact.models import (
    ExpertProfile,
    MemberProfile,
)


class TestUtils(TestCase):
    def test_get_profile_for_expert(self):
        user = UserContext("EXPERT").user
        assert isinstance(get_profile(user), ExpertProfile)

    def test_get_profile_for_member(self):
        user = UserContext("MEMBER").user
        assert isinstance(get_profile(user), MemberProfile)
