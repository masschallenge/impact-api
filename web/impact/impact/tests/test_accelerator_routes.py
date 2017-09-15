# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from test_plus.test import TestCase
from impact.urls import accelerator_router
from django.apps import apps
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType
from impact.tests.factories.accelerator import (
    StartupFactory,
    IndustryFactory)
from django.contrib.auth.models import Permission
import simplejson as json

from impact.tests.factories import UserFactory
from impact.tests.factories import ContentTypeFactory
from impact.tests.factories import PermissionFactory


class TestAcceleratorRoutes(TestCase):
    client_class = APIClient
    user_factory = UserFactory

    @classmethod
    def setUpClass(cls):
        ContentTypeFactory(app_label='mc', model='startup')
        ContentTypeFactory(app_label='mc', model='organization')
        ContentTypeFactory(app_label='mc', model='recommendationtag')

    @classmethod
    def tearDownClass(cls):
        ContentType.objects.filter(
            app_label='mc',
            model__in=[
                'startup',
                'organization',
                'recommendationtag']).delete()

    def test_api_object_list(self):
        StartupFactory(is_visible=1)
        StartupFactory(is_visible=1)
        StartupFactory(is_visible=1)
        url_name = "object-list"
        view_kwargs = {'app': 'accelerator', "model": "startup"}
        self.response_401(self.get(url_name, **view_kwargs))

        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            self.response_403(self.get(url_name, **view_kwargs))
        startup_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startup'),
            codename='view_startup',
        )
        perm_user = self.make_user(
            'perm_user2@test.com', perms=["mc.view_startup"])
        perm = PermissionFactory.create(codename='change_startup')
        view_perm = PermissionFactory.create(codename='view_startup')
        perm_user.user_permissions.add(perm)
        perm_user.user_permissions.add(startup_permission)
        perm_user.user_permissions.add(view_perm)
        perm_user.save()
        with self.login(perm_user):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("short_pitch", response_dict['results'][0].keys())
            for startup in response_dict['results']:
                self.assertEqual(startup["is_visible"], 1)

    def test_api_object_get(self):
        url_name = "object-detail"
        industry = IndustryFactory()
        StartupFactory(id=1, primary_industry_id=industry.id)
        view_kwargs = {
            'app': 'accelerator',
            "model": "startup",
            "pk": 1,
        }
        self.response_401(self.get(url_name, **view_kwargs))
        startup_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startup'),
            codename='view_startup',
        )
        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            self.response_403(self.get(url_name, **view_kwargs))

        perm_user = self.make_user(
            'perm_user@test.com', perms=["mc.view_startup"])
        perm = PermissionFactory.create(codename='change_startup')
        view_perm = PermissionFactory.create(codename='view_startup')
        perm_user.user_permissions.add(perm)
        perm_user.user_permissions.add(startup_permission)
        perm_user.user_permissions.add(view_perm)
        perm_user.save()
        with self.login(perm_user):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("is_visible", response_dict.keys())

    def test_accelerator_app_is_registered(self):
        urls = [url for url in accelerator_router.get_urls() if (
            url.name != 'api-root')]
        url_count = len(urls)
        accelerate_models = [
            model for model in apps.get_models('accelerator') if (
                model._meta.app_label == 'accelerator' and hasattr(
                    model, "Meta"))]
        model_count = len(accelerate_models)
        # we should have two detail and list views per model
        self.assertEquals(
            model_count * 4,
            url_count)
