# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.test import TestCase


class TestCorsSetup(TestCase):

    def test_expose_headers(self):
        resp = self.client.get('/', HTTP_ORIGIN='http://thirdparty.com')
        self.assertEqual(
            resp['access-control-allow-credentials'], 'true')
