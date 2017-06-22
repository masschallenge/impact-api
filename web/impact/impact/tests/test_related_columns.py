# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    ContentType,
    Permission,
)
from django.urls import reverse
from rest_framework.test import APIClient
from test_plus.test import TestCase

from impact.tests.factories import (
    ContentTypeFactory,
    PermissionFactory,
    StartupTeamMemberFactory,
)


class TestRelatedColumns(TestCase):
    client_class = APIClient

    @classmethod
    def tearDownClass(cls):
        ContentType.objects.filter(
            app_label='mc',
            model__in=[
                'startup',
                'startupteammember',
                'user']).delete()

    @classmethod
    def setUpClass(cls):
        startup_ctype = ContentTypeFactory(app_label='mc', model='startup')
        teammember_ctype = ContentTypeFactory(app_label='mc',
                                              model='startupteammember')
        ContentTypeFactory(app_label='mc', model='user')
        Permission.objects.get_or_create(
            content_type=startup_ctype,
            codename='view_startup_stealth_mode_true',
            name='Can view Startups in Stealth Mode',
        )
        Permission.objects.get_or_create(
            content_type=teammember_ctype,
            codename='view_startupteammember',
        )

    def test_api_object_relation_link_is_valid(self):
        url_name = "object-list"
        view_kwargs = {'app': 'impact', "model": "startupteammember"}
        StartupTeamMemberFactory()
        User = get_user_model()
        perm = PermissionFactory.create(codename='change_user')
        user = User.objects.create_superuser("admin@test.com", "password")
        startup_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startup'),
            codename='view_startup_stealth_mode_true',
            name='Can view Startups in Stealth Mode',
        )
        startup_member_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startupteammember'),
            codename='view_startupteammember',
        )
        user_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='simpleuser',
                model='user'),
            codename='view_user',
        )
        user.user_permissions.add(user_permission)
        user.user_permissions.add(perm)
        user.user_permissions.add(startup_permission)
        user.user_permissions.add(startup_member_permission)
        user.save()

        with self.login(username="admin@test.com"):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)

            response_dict = json.loads(response.content)
            self.assertIn("user", response_dict['results'][0].keys())
            entrepreneur_id = response_dict['results'][0]['user']
            detail_args = {'app': 'simpleuser', "model": "user"}

            detail_args['pk'] = entrepreneur_id
            detail_response = self.get('object-detail', **detail_args)
            detail_json = json.loads(detail_response.content)
            self.assertEqual(detail_json['id'], entrepreneur_id)

    def test_api_list_contains_url_to_related_object(self):
        url_name = "object-list"
        view_kwargs = {'app': 'impact', "model": "startupteammember"}
        StartupTeamMemberFactory()
        User = get_user_model()
        user = User.objects.create_superuser("admin@test.com", "password")
        perm = PermissionFactory.create(codename='change_user')
        startup_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startup'),
            codename='view_startup_stealth_mode_true',
            name='Can view Startups in Stealth Mode',
        )
        _, startupteammember_permission = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='mc',
                model='startupteammember'),
            codename='view_startupteammember',
        )
        user.user_permissions.add(perm)
        user.user_permissions.add(startup_permission)
        user.user_permissions.add(startupteammember_permission)
        user.save()
        with self.login(username="admin@test.com"):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("user", response_dict['results'][0].keys())
            entrepreneur_id = response_dict['results'][0]['user']
            detail_args = {'app': 'simpleuser', "model": "user"}
            detail_args['pk'] = entrepreneur_id
            detail_url = reverse('object-detail', kwargs=detail_args)
            absolute_uri = response.wsgi_request.build_absolute_uri(
                detail_url)
            detail_args['pk'] = response_dict['results'][0]['user']
            returned_uri = response.wsgi_request.build_absolute_uri(
                reverse('object-detail',
                        kwargs=detail_args))
            self.assertEqual(
                returned_uri,
                absolute_uri)
