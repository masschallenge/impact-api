# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from oauth2_provider.models import get_application_model
from rest_framework.test import APIClient
from test_plus.test import TestCase

from django.core import mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import reverse

from accelerator_abstract.models.base_clearance import (
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    CLEARANCE_LEVEL_STAFF
)
from impact.tests.factories import (
    ClearanceFactory,
    UserFactory,
)

OAuth_App = get_application_model()
API_GROUPS = [settings.V0_API_GROUP, settings.V1_API_GROUP]


class APITestCase(TestCase):
    SOME_SITE_NAME = "somesite.com"
    _user_count = 0
    client_class = APIClient
    user_factory = UserFactory

    @classmethod
    def setUpClass(cls):
        [Group.objects.get_or_create(name=name) for name in API_GROUPS]

    @classmethod
    def tearDownClass(cls):
        [Group.objects.get(name=name).delete() for name in API_GROUPS]

    def basic_user(self):
        user = self.make_user('basic_user{}@test.com'.format(self._user_count),
                              perms=["mc.view_startup"])
        self._user_count += 1
        for group in Group.objects.filter(name__in=API_GROUPS):
            user.groups.add(group)
        user.set_password('password')
        user.save()
        return user

    def staff_user(self):
        user = self.make_user('basic_user{}@test.com'.format(self._user_count))
        self._user_count += 1
        clearance = ClearanceFactory(
            level=CLEARANCE_LEVEL_STAFF,
            user=user)
        return clearance.user

    def global_operations_manager(self, program_family):
        user = self.staff_user()
        ClearanceFactory(user=user,
                         level=CLEARANCE_LEVEL_GLOBAL_MANAGER,
                         program_family=program_family)
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

    def assert_options_include(self, method, expected_options, object_id=None):
        if object_id:
            args = [object_id]
        else:
            args = []
        url = reverse(self.view.view_name, args=args)
        with self.login(email=self.basic_user().email):
            response = self.client.options(url)
            result = json.loads(response.content)
            assert method in result['actions']
            options = result['actions'][method]['properties']
            for key, params in expected_options.items():
                self.assertIn(key, options)
                self.assertEqual(options[key], params)

    def assert_ui_notification(self, response, success, notification):
        data = response.data
        header = self.success_header if success else self.fail_header
        self.assertTrue(all([
            data['success'] == success,
            data['header'] == header,
            data['detail'] == notification
        ]), msg='Notification data was not as expected')

    def assert_notified(self, user, message=""):
        '''Assert that the user received a notification. 
        If `message` is specified, assert that the message appears in one of 
        the outgoing emails to this user
        '''
        emails = [email for email in mail.outbox if user.email in email.to]
        self.assertGreater(len(emails), 0)
        if message:    
            self.assertTrue(any([message in email.body for email in emails]))


    def assert_not_notified(self, user):
        '''Assert that the specified user did not receive a notification.
        '''
        if mail.outbox:
            self.assertNotIn(user.email, [email.to for email in mail.outbox],
                             msg="Found an email sent to user")

        
