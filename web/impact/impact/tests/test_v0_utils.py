# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from impact.v0.views.utils import (
    logo_url,
    pad_slash,
)
from impact.tests.factories import StartupFactory

REMOTE_URL = "http://cloud.test.com/logo.jpg"

URL_WITHOUT_TRAILING_SLASH = "http://cloud.test.com"


class TestUtils(TestCase):
    def test_logo_url_returns_url_as_is_if_remote_url(self):
        startup = StartupFactory(high_resolution_logo=REMOTE_URL)

        assert REMOTE_URL == logo_url(startup)

    def test_pad_slash_pads_slash_correctly(self):
        assert URL_WITHOUT_TRAILING_SLASH + "/" == pad_slash(
            URL_WITHOUT_TRAILING_SLASH)
