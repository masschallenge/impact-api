# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.test import TestCase
from django.conf import settings


class TestCorsSetup(TestCase):

    def test_expose_headers(self):
        local_url = "http://" + settings.CORS_ORIGIN_WHITELIST[0]
        resp = self.client.get('/', HTTP_ORIGIN=local_url)
        self.assertEqual(
            resp['access-control-allow-credentials'], 'true')
