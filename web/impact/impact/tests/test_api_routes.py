# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from mc.models import ProgramRole
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from test_plus.test import TestCase

from .factories import (
    ProgramRoleFactory,
    StartupStatusFactory,
    UserFactory,
)
from .factories import (
    PermissionFactory,
    StartupFactory,
)

from ..v1.views.user_detail_view import UserDetailView


class TestApiRoute(TestCase):
    client_class = APIClient
    user_factory = UserFactory

    def test_api_object_list(self):
        StartupFactory(is_visible=1, organization__url_slug="test1")
        StartupFactory(is_visible=1, organization__url_slug="test2")
        StartupFactory(is_visible=1, organization__url_slug="test3")
        Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='startup'),
            codename='view_startup_stealth_mode_false'
        )
        view_perm, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='startup'),
            codename='view_startup'
        )
        url_name = "object-list"
        view_kwargs = {'app': 'accelerator', "model": "startup"}
        self.response_401(self.get(url_name, **view_kwargs))

        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            self.response_403(self.get(url_name, **view_kwargs))

        perm_user = self.make_user(
            'perm_user@test.com', perms=["mc.view_startup"])
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
        StartupFactory(id=1)
        view_kwargs = {
            'app': 'accelerator',
            "model": "startup",
            "pk": 1,
        }
        self.response_401(self.get(url_name, **view_kwargs))
        startup_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
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

    def test_api_related_object_list_get(self):
        StartupFactory(is_visible=1, organization__url_slug="test1")
        StartupFactory(is_visible=1, organization__url_slug="test2")
        StartupFactory(is_visible=1, organization__url_slug="test3")
        view_perm, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='startup'),
            codename='view_startup_additional_industries'
        )
        url_name = "related-object-list"
        view_kwargs = {"app": "accelerator",
                       "model": "startup",
                       "related_model": "additional_industries"}
        self.response_401(self.get(url_name, **view_kwargs))

        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            self.response_403(self.get(url_name, **view_kwargs))

        perm_user = self.make_user(
            'perm_user@test.com',
            perms=["mc.view_startup_additional_industries"])
        perm_user.user_permissions.add(view_perm)
        with self.login(perm_user):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)

    def test_basic_user_without_permissions_cannot_create_object(self):
        url_name = "object-list"
        program_role = ProgramRoleFactory(id=1)
        startup_status = StartupStatusFactory(id=1)
        view_kwargs = {
            'app': 'accelerator',
            "model": "programrole",
        }
        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            response = self.post(url_name, data={
                "name": "2011 - Final",
                "program": program_role.id,
                "user_role": startup_status.id}, **view_kwargs)
            self.response_403(response)
            self.assertFalse(
                ProgramRole.objects.filter(name="2011 - Final").exists())

    def test_anonymous_user_cannot_create_object(self):
        url_name = "object-list"
        program_role = ProgramRoleFactory(id=1)
        startup_status = StartupStatusFactory(id=1)
        view_kwargs = {
            'app': 'accelerator',
            "model": "programrole",
        }
        response = self.post(url_name, data={
            "name": "2011 - Final",
            "program": program_role.id,
            "user_role": startup_status.id}, **view_kwargs)
        self.response_401(response)
        self.assertFalse(
            ProgramRole.objects.filter(name="2011 - Final").exists())

    def test_user_with_permissions_can_create_objects(self):
        url_name = "object-list"
        program_role = ProgramRoleFactory(id=1)
        startup_status = StartupStatusFactory(id=1)
        view_kwargs = {
            'app': 'accelerator',
            "model": "programrole",
        }
        self.response_401(self.get(url_name, **view_kwargs))
        program_role_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='programrole'),
            codename='add_programrole',
        )
        perm_user = self.make_user(
            'perm_user@test.com', perms=["mc.add_programrole"])
        perm = PermissionFactory.create(codename='change_programrole')
        view_perm = PermissionFactory.create(codename='view_programrole')
        perm_user.user_permissions.add(perm)
        perm_user.user_permissions.add(program_role_permission)
        perm_user.user_permissions.add(view_perm)
        perm_user.save()
        self.assertFalse(
            ProgramRole.objects.filter(name="2011 - Final").exists())
        with self.login(perm_user):
            self.post(url_name, data={
                "name": "2011 - Final",
                "program": program_role.id,
                "user_role": startup_status.id}, **view_kwargs)
            self.assertTrue(
                ProgramRole.objects.filter(name="2011 - Final").exists())

    def test_api_object_delete(self):
        StartupFactory(id=2)
        url_name = "object-detail"
        view_kwargs = {
            'app': 'accelerator',
            "model": "startup",
            "pk": 2,
        }
        self.response_401(self.get(url_name, **view_kwargs))

        basic_user = self.make_user('basic_user@test.com')
        startup_delete_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='startup'),
            codename='delete_startup',
        )
        startup_view_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='startup'),
            codename='delete_startup',
        )
        with self.login(basic_user):
            response = self.get(url_name, **view_kwargs)
            self.response_403(response)
        perm_user = self.make_user(
            'perm_user@test.com',
            perms=[
                "mc.view_startup",
                "mc.change_startup",
                "mc.delete_startup"])
        perm = PermissionFactory.create(codename='change_startup')
        perm_user.user_permissions.add(perm)
        perm_user.user_permissions.add(startup_delete_permission)
        perm_user.user_permissions.add(startup_view_permission)
        perm_user.save()
        with self.login(perm_user):
            self.delete(url_name, **view_kwargs)
            self.assertEqual(204, self.last_response.status_code)

    def test_api_object_get_field_filter(self):
        startup_content_type = ContentType.objects.get(
            app_label='accelerator',
            model='startup')
        stealth_perm = PermissionFactory(
            content_type=startup_content_type,
            codename='view_startup_stealth_mode_true')
        StartupFactory(id=3, is_visible=0)
        url_name = "object-detail"
        view_kwargs = {
            'app': 'accelerator',
            "model": "startup",
            "pk": 3,  # has stealth mode enabled
        }
        response = self.get(url_name, **view_kwargs)
        self.response_401(response)

        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            response = self.get(url_name, **view_kwargs)
            self.response_403(response)

        change_perm = Permission.objects.get(codename='change_startup',
                                             content_type=startup_content_type)
        view_perm = Permission.objects.get(codename='view_startup',
                                           content_type=startup_content_type)
        perm_user = self.make_user('perm_user@test.com',
                                   perms=["mc.view_startup"])
        with self.login(perm_user):
            self.response_403(self.get(url_name, **view_kwargs))

        correct_perm_user = self.make_user(
            'correct_perm_user@test.com',
            perms=[
                "mc.view_startup",
                "mc.change_startup",
                "mc.view_startup_stealth_mode_true"
            ])
        correct_perm_user.user_permissions.add(change_perm)
        correct_perm_user.user_permissions.add(view_perm)
        correct_perm_user.user_permissions.add(stealth_perm)
        with self.login(correct_perm_user):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("is_visible", response_dict.keys())

    def test_api_object_put(self):
        url_name = "object-detail"
        startup = StartupFactory(id=1, is_visible=False)
        get_kwargs = {
            'app': 'accelerator',
            "model": "startup",
            "pk": 1,
        }
        data = json.dumps({
            "is_visible": True,
            "name": "test",
            "primary_industry": startup.primary_industry.id,
            "short_pitch": "test",
            "full_elevator_pitch": "test",
            "website_url": "http://test.com",
            "linked_in_url": "http://test.com",
            "facebook_url": "http://test.com",
            "twitter_handle": "@test",
            "public_inquiry_email": "test@test.com",
            "video_elevator_pitch_url": "http://example.com",
            "user": startup.user.id,
            "created_datetime": None,
            "last_updated_datetime": None,
            "community": "red",
            "url_slug": "testing",
            "profile_background_color": "000000",
            "profile_text_color": "FFFFFF",
            "currency": "",
            "date_founded": "test",
            "location_city": "test",
            "location_national": "test",
            "location_postcode": "test",
            "location_regional": "test",
            "landing_page": "test"
        })  # field "high_resolution_logo" was removed, to be solved in AC-4750
        extra = {"content_type": "application/json"}
        put_kwargs = get_kwargs.copy()
        put_kwargs["data"] = data
        put_kwargs["extra"] = extra

        self.response_401(self.put(url_name, **put_kwargs))

        basic_user = self.make_user('basic_user@test.com')
        with self.login(basic_user):
            self.response_403(self.get(url_name, **get_kwargs))
        startup_content_type = ContentType.objects.get(
            app_label='accelerator',
            model='startup')
        stealth_startup_permission, _ = Permission.objects.get_or_create(
            content_type=startup_content_type,
            codename='view_startup_is_visible_false')
        invisible_startup_view_permission, _ = (
            Permission.objects.get_or_create(
                content_type=startup_content_type,
                codename='view_startup_is_visible_false'))
        visible_startup_change_permission, _ = (
            Permission.objects.get_or_create(
                content_type=startup_content_type,
                codename='change_startup_is_visible_true'))
        stealth_startup_change_permission, _ = (
            Permission.objects.get_or_create(
                content_type=startup_content_type,
                codename='change_startup_is_visible_false'))
        visible_startup_view_permission, _ = Permission.objects.get_or_create(
            content_type=startup_content_type,
            codename='view_startup_is_visible_true')
        startup_member_permission, _ = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='accelerator',
                model='startupteammember'),
            codename='view_startupteammember',
        )
        startup_permission, _ = Permission.objects.get_or_create(
            content_type=startup_content_type,
            codename='view_startup',
        )
        change_startup_permission, _ = Permission.objects.get_or_create(
            content_type=startup_content_type,
            codename='change_startup', )
        perm_user = self.make_user(
            'perm_user@test.com')
        perm_user.user_permissions.add(startup_permission)
        perm_user.user_permissions.add(stealth_startup_permission)
        perm_user.user_permissions.add(change_startup_permission)
        perm_user.user_permissions.add(visible_startup_view_permission)
        perm_user.user_permissions.add(visible_startup_change_permission)
        perm_user.user_permissions.add(startup_member_permission)
        perm_user.user_permissions.add(invisible_startup_view_permission)
        perm_user.user_permissions.add(stealth_startup_change_permission)
        perm_user.save()
        with self.login(perm_user):
            response = self.get(url_name, **get_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("is_visible", response_dict.keys())
            self.assertEqual(response_dict["is_visible"], False)
            # we can now put a different value
            response = self.put(url_name, **put_kwargs)
            self.response_200(response)
            response_dict = json.loads(response.content)
            self.assertIn("is_visible", response_dict.keys())
            self.assertEqual(response_dict["is_visible"], True)

    def test_current_user_can_view_their_user_detail_page(self):
        url_name = UserDetailView.view_name
        basic_user = self.make_user('basic_user@test.com')
        view_kwargs = {"pk": basic_user.id}

        response = self.get(url_name, **view_kwargs)
        self.response_401(response)

        with self.login(basic_user):
            response = self.get(url_name, **view_kwargs)
            self.response_200(response)
