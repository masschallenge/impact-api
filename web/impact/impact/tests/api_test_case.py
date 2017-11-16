# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import simplejson as json
from oauth2_provider.models import get_application_model
from rest_framework.test import APIClient
from test_plus.test import TestCase

from django.conf import settings
from django.contrib.auth.models import Group

from impact.tests.factories import UserFactory

OAuth_App = get_application_model()
API_GROUPS = [settings.V0_API_GROUP, settings.V1_API_GROUP]


class APITestCase(TestCase):
    SOME_SITE_NAME = "somesite.com"

    client_class = APIClient
    user_factory = UserFactory

    @classmethod
    def setUpClass(cls):
        [Group.objects.get_or_create(name=name) for name in API_GROUPS]

    @classmethod
    def tearDownClass(cls):
        [Group.objects.get(name=name).delete() for name in API_GROUPS]

    def basic_user(self):
        user = self.make_user('basic_user@test.com',
                              perms=["mc.view_startup"])
        [user.groups.add(group)
         for group in Group.objects.filter(name__in=API_GROUPS)]
        user.set_password('password')
        user.save()
        return user

    def get_access_token(self, user):
        app = OAuth_App.objects.create(
            user=user,
            name="Test666",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://thirdparty.com/exchange/",
        )
        response = self.client.post(
            self.reverse("oauth2_provider:token"),
            data={
                "password": 'password',
                "client_id": app.client_id,
                "username": user.username,
                "grant_type": "password",
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response_json = json.loads(response.content)
        return response_json['access_token']
