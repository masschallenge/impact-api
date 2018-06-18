# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import simplejson as json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from accelerator.models import UserRole
from accelerator.tests.factories import (
    NamedGroupFactory,
    ProgramFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
    UserRoleFactory,
)
from accelerator_abstract.models import (
    ACTIVE_PROGRAM_STATUS,
    UPCOMING_PROGRAM_STATUS,
)
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import UserFactory
from impact.views import AlgoliaApiKeyView
from impact.views.algolia_api_key_view import IS_CONFIRMED_MENTOR_FILTER

User = get_user_model()  # pylint: disable=invalid-name


class TestAlgoliaApiKeyView(APITestCase):
    client_class = APIClient
    user_factory = UserFactory
    url = reverse(AlgoliaApiKeyView.view_name)

    def test_logged_in_user_generates_token(self):
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=self.basic_user().email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)
                self.assertTrue('token' in response_data.keys())

    def test_unauthenticated_user_is_denied(self):
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            response = self.client.get(self.url)
            response_data = json.loads(response.content)
            self.assertTrue(
                response_data['detail'] == 'Authentication credentials '
                                           'were not provided.')

    def test_staff_user_gets_empty_filters(self):
        user = self.basic_user()
        user.is_staff = True
        user.save()
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)
                self.assertEqual(response_data["filters"], [])

    def test_finalist_user_gets_all_programs_in_program_group(self):
        named_group = NamedGroupFactory()
        programs = []
        for _ in range(5):
            programs.append(ProgramFactory(
                mentor_program_group=named_group,
                program_status=ACTIVE_PROGRAM_STATUS))
        other_program = ProgramFactory(program_status=ACTIVE_PROGRAM_STATUS)
        program = programs[0]
        user = self._create_user_with_role_grant(program, UserRole.FINALIST)
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)

                for program in programs:
                    self.assertIn(program.name, response_data["filters"])
                self.assertNotIn(other_program.name, response_data["filters"])

    def test_finalist_user_gets_all_programs_in_past_or_present(self):
        named_group = NamedGroupFactory()
        programs = []
        for _ in range(5):
            programs.append(ProgramFactory(
                mentor_program_group=named_group,
                program_status=ACTIVE_PROGRAM_STATUS))
        other_program = ProgramFactory(program_status=UPCOMING_PROGRAM_STATUS,
                                       mentor_program_group=named_group)
        program = programs[0]
        user = self._create_user_with_role_grant(program, UserRole.FINALIST)
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)

                for program in programs:
                    self.assertIn(program.name, response_data["filters"])
                self.assertNotIn(other_program.name, response_data["filters"])

    def test_non_participant_user_sees_all_confirmed_mentors(self):
        named_group = NamedGroupFactory()
        programs = []
        for _ in range(5):
            programs.append(ProgramFactory(
                mentor_program_group=named_group,
                program_status=ACTIVE_PROGRAM_STATUS))
        program = programs[0]
        user = self._create_user_with_role_grant(program,
                                                 UserRole.DESIRED_MENTOR)
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)

                self.assertIn(IS_CONFIRMED_MENTOR_FILTER,
                              response_data["filters"])

    def _create_user_with_role_grant(self, program, user_role_name):
        user_role = UserRoleFactory(name=user_role_name)
        program_role = ProgramRoleFactory(
            user_role=user_role,
            program=program
        )
        user = self.basic_user()
        ProgramRoleGrantFactory(person=user, program_role=program_role)
        return user
