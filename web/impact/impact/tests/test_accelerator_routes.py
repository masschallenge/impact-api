import json
from test_plus.test import TestCase

from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient

from accelerator.tests.factories import (
    StartupFactory,
    IndustryFactory,
)
from accelerator.tests.factories.organization_factory import (
    OrganizationFactory
)
from mc.models import Startup

from ..urls import schema_router
from .factories import (
    PermissionFactory,
    StartupStatusFactory,
    UserFactory,
)
from ..views.general_view_set import (
    MODELS_TO_EXCLUDE_FROM_URL_BINDING
)

VIEWS_PER_MODEL = 4

MC_CONTENTTYPES = [
    'startup',
    'organization',
    'programrole',
]


class TestAcceleratorRoutes(TestCase):
    client_class = APIClient
    user_factory = UserFactory

    def _grant_permissions(
            self,
            user,
            model_name,
            permissions=['change', 'view', 'add']):
        for action in permissions:
            permission = PermissionFactory.create(
                codename='{action}_{model_name}'.format(
                    action=action,
                    model_name=model_name))
            user.user_permissions.add(permission)
        user.save()

    def test_user_with_permissions_can_create_objects(self):
        url_name = "object-list"
        StartupStatusFactory()
        view_kwargs = {
            'app': 'mc',
            "model": "startup",
        }
        self.response_401(self.get(url_name, **view_kwargs))
        startup_add_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startup'),
            codename='add_startup',
        )
        perm_user = self.make_user(
            'perm_user2@test.com')
        self._grant_permissions(
            perm_user,
            model_name='startup',
            permissions=['add', 'change', 'view'])
        org = OrganizationFactory()
        industry = IndustryFactory()
        self.assertFalse(
            Startup.objects.filter(organization=org).exists())
        with self.login(perm_user):
            self.post(url_name, data={
                "is_visible": False,
                "full_elevator_pitch": "test",
                "linked_in_url": "",
                "short_pitch": "test",
                "facebook_url": "",
                "video_elevator_pitch_url": "",
                "organization": org.id,
                "user": perm_user.id,
                "primary_industry": industry.id
            }, **view_kwargs)
            org_query = Startup.objects.filter(organization=org)
            self.assertTrue(
                org_query.exists())
            self.assertTrue(
                org_query.first().primary_industry.id == industry.id)

    def test_api_object_list(self):
        StartupFactory.create_batch(size=4, is_visible=1)
        url_name = "object-list"
        view_kwargs = {'app': 'mc', "model": "startup"}
        self.response_401(self.get(url_name, **view_kwargs))

        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            self.response_403(self.get(url_name, **view_kwargs))
        perm_user = self.make_user(
            'perm_user2@test.com')
        self._grant_permissions(
            perm_user,
            model_name='startup',
            permissions=['view', 'change'])
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
            'app': 'mc',
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
            'perm_user@test.com')
        self._grant_permissions(
            perm_user,
            model_name='startup',
            permissions=['view'])
        with self.login(perm_user):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("is_visible", response_dict.keys())

    def test_accelerator_app_is_registered(self):
        urls = [url for url in schema_router.get_urls() if (
            url.name != 'api-root')]
        url_count = len(urls)
        accelerate_models = [
            model for model in apps.get_models('mc') if (
                model._meta.app_label == 'mc' and hasattr(
                    model, "Meta") and
                model.__name__ not in MODELS_TO_EXCLUDE_FROM_URL_BINDING)]
        model_count = len(accelerate_models)
        # we should have two detail and list views per model
        self.assertEqual(model_count * VIEWS_PER_MODEL, url_count)
