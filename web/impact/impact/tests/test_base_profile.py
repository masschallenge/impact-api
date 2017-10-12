from impact.tests.api_test_case import APITestCase
from impact.tests.factories import BaseProfileFactory


class TestBaseProfile(APITestCase):
    def test_str(self):
        base_profile = BaseProfileFactory()
        bp_string = str(base_profile)
        assert base_profile.user.short_name in bp_string
        assert base_profile.user.full_name in bp_string

    def test_str_with_partial_name(self):
        base_profile = BaseProfileFactory(user__full_name="")
        bp_string = str(base_profile)
        assert base_profile.user.short_name not in bp_string
        assert base_profile.user.username in bp_string
