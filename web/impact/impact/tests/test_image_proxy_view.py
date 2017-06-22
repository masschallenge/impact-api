# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from unittest.mock import patch
from django.http import HttpResponse
from django.conf import settings

from django.contrib.auth.models import Group
from impact.tests.api_v0_test_case import APIV0TestCase
from impact.tests.utils import match_errors
from impact.v0.views import ImageProxyView


class TestImageProxyView(APIV0TestCase):
    def test_proxy_images_view(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        basic_user.set_password('password')
        basic_user.save()
        v0_group = Group.objects.get(
            name=settings.V0_API_GROUP)
        basic_user.groups.add(v0_group)
        access_token = self.get_access_token(basic_user)
        with patch.object(ImageProxyView, 'proxy') as patched_proxy:
            patched_proxy.return_value = HttpResponse()
            self.client.get(
                self.reverse("image"),
                data={
                    "ImageToken": "TOKEN_TOKEN",
                }, headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                }, HTTP_AUTHORIZATION='Bearer %s' % access_token)
            patched_proxy.assert_called()

    def test_proxy_images_view_requires_v0_permissions(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        basic_user.set_password('password')
        basic_user.save()
        access_token = self.get_access_token(basic_user)
        with patch.object(ImageProxyView, 'proxy') as patched_proxy:
            patched_proxy.return_value = HttpResponse()
            self.client.get(
                self.reverse("image"),
                data={
                    "ImageToken": "TOKEN_TOKEN",
                }, headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                }, HTTP_AUTHORIZATION='Bearer %s' % access_token)
            patched_proxy.assert_not_called()

    def test_proxy_images_view_requires_authorization(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        basic_user.set_password('password')
        basic_user.save()
        self.get_access_token(basic_user)
        response = self.client.get(
            self.reverse("image"),
            data={
                "ImageToken": "TOKEN_TOKEN",
            }, headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            }, HTTP_AUTHORIZATION='Bearer invalid_token')
        self.response_401(response)

    def test_proxy_images_view_invalid_params(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        basic_user.set_password('password')
        basic_user.save()
        v0_group = Group.objects.get(
            name=settings.V0_API_GROUP)
        basic_user.groups.add(v0_group)
        access_token = self.get_access_token(basic_user)
        response = self.client.get(
            self.reverse("image"),
            data={
                'SiteName': self.SOME_SITE_NAME,
            }, headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            }, HTTP_AUTHORIZATION='Bearer %s' % access_token)
        assert 404 == response.status_code
        assert match_errors({"SiteName": "deprecated",
                             "ImageToken": "not found"},
                            response.data)

    def test_proxy_images_view_missing_settings(self):
        basic_user = self.make_user(
            'basic_user@test.com', perms=["mc.view_startup"])
        basic_user.set_password('password')
        basic_user.save()
        v0_group = Group.objects.get(
            name=settings.V0_API_GROUP)
        basic_user.groups.add(v0_group)
        access_token = self.get_access_token(basic_user)
        with self.settings(V0_SITE_NAME=""):
            response = self.client.get(
                self.reverse("image"),
                data={
                    "ImageToken": "TOKEN_TOKEN",
                    }, headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    }, HTTP_AUTHORIZATION='Bearer %s' % access_token)
            assert 404 == response.status_code
            assert match_errors({"Default SiteName": "not set"},
                                response.data)

    def test_create_response(self):
        assert ImageProxyView().create_response(HttpResponse())
