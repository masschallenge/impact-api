# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from unittest.mock import patch

from django.http import HttpResponse
from django.conf import settings

from django.contrib.auth.models import Group
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import match_errors
from impact.v0.views import MentorsProxyView


class TestMentorsProxyView(APITestCase):
    SOME_SECURITY_KEY = "Some Secret Security Key"

    def setUp(self):
        self.data = {'NumItems': 100,
                     'GroupBy': 'Industry',
                     'ProgramKey': 'MassChallenge+Boston+2016+Accelerator'}
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/x-www-form-urlencoded'}
        self.url = self.reverse("mentors")

    def test_proxy_mentors_view(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        v0_group = Group.objects.get(
            name=settings.V0_API_GROUP)
        basic_user.groups.add(v0_group)
        basic_user.set_password('password')
        basic_user.save()
        access_token = self.get_access_token(basic_user)
        with patch.object(MentorsProxyView, 'proxy') as patched_proxy:
            patched_proxy.return_value = HttpResponse()
            self.client.post(
                self.url, data=self.data, headers=self.headers,
                HTTP_AUTHORIZATION='Bearer %s' % access_token)
            patched_proxy.assert_called()

    def test_proxy_mentors_view_requires_v0_permissions(self):
        user_without_permissions = self.make_user(
            'user_without_permissions@test.com', perms=["mc.view_startup"])
        user_without_permissions.set_password('password')
        user_without_permissions.save()
        access_token = self.get_access_token(user_without_permissions)
        with patch.object(MentorsProxyView, 'proxy') as patched_proxy:
            patched_proxy.return_value = HttpResponse()
            self.client.post(
                self.url, data=self.data, headers=self.headers,
                HTTP_AUTHORIZATION='Bearer %s' % access_token)
            patched_proxy.assert_not_called()

    def test_proxy_mentors_view_requires_authorization(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        basic_user.set_password('password')
        basic_user.save()
        self.get_access_token(basic_user)
        response = self.client.post(
            self.url, data=self.data, headers=self.headers,
            HTTP_AUTHORIZATION='Bearer invalid_token')
        self.response_401(response)

    def test_proxy_mentors_view_invalid_params(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        v0_group = Group.objects.get(
            name=settings.V0_API_GROUP)
        basic_user.groups.add(v0_group)
        basic_user.set_password('password')
        basic_user.save()
        access_token = self.get_access_token(basic_user)
        self.data.update({'SiteName': self.SOME_SITE_NAME,
                         'SecurityKey': self.SOME_SECURITY_KEY})
        response = self.client.post(
            self.url, data=self.data, headers=self.headers,
            HTTP_AUTHORIZATION='Bearer %s' % access_token)
        assert 404 == response.status_code
        assert match_errors({"SiteName": "deprecated",
                             "SecurityKey": "deprecated"},
                            response.data)

    def test_proxy_mentors_view_missing_settings(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        v0_group = Group.objects.get(
            name=settings.V0_API_GROUP)
        basic_user.groups.add(v0_group)
        basic_user.set_password('password')
        basic_user.save()
        access_token = self.get_access_token(basic_user)
        with self.settings(V0_SITE_NAME="",
                           V0_SECURITY_KEY=""):
            response = self.client.post(
                self.url, data=self.data, headers=self.headers,
                HTTP_AUTHORIZATION='Bearer %s' % access_token)
            assert 404 == response.status_code
            assert match_errors({"Default SiteName": "not set",
                                 "Default SecurityKey": "not set"},
                                response.data)
