# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestUser(TestCase):

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user()
