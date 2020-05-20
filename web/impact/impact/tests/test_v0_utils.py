# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase

from .factories import StartupFactory
from .v0.views.utils import (
    logo_url,
    pad_slash,
)

URL_WITHOUT_TRAILING_SLASH = "http://cloud.test.com"


class TestUtils(TestCase):
    def test_logo_url_returns_empty_string_if_none(self):
        startup = StartupFactory(high_resolution_logo=None)
        assert logo_url(startup) == ""

    def test_pad_slash_pads_slash_correctly(self):
        assert URL_WITHOUT_TRAILING_SLASH + "/" == pad_slash(
            URL_WITHOUT_TRAILING_SLASH)
