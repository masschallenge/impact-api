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
    EntrepreneurFactory,
    ExpertFactory,
)
from accelerator_abstract.models import (
    ACTIVE_PROGRAM_STATUS,
    UPCOMING_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS,
    ENTREPRENEUR_USER_TYPE
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

    def test_logged_in_user_with_no_role_grant_gets_403(self):
        user = self._create_entrepreneur()
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                self.assertTrue(response.status_code, 403)

    def test_logged_in_user_with_role_grants_in_ended_programs_gets_403(self):
        named_group = NamedGroupFactory()
        program = ProgramFactory(
            mentor_program_group=named_group,
            program_status=ENDED_PROGRAM_STATUS)
        user = self._create_user_with_role_grant(program, UserRole.FINALIST)
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                self.assertTrue(response.status_code, 403)

    def test_logged_in_user_generates_token(self):
        named_group = NamedGroupFactory()
        program = ProgramFactory(
            mentor_program_group=named_group,
            program_status=ACTIVE_PROGRAM_STATUS)
        user = self._create_user_with_role_grant(program, UserRole.FINALIST)
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
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

    def test_entrepreneur_that_never_had_a_finalist_role_gets_403(self):
        user = self._create_entrepreneur()
        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                self.assertTrue(response.status_code, 403)

    def test_user_with_staff_role_grant_sees_all_mentors(self):
        user = self.basic_user()

        named_group = NamedGroupFactory()
        program = ProgramFactory(
            mentor_program_group=named_group,
            program_status=ACTIVE_PROGRAM_STATUS)
        self._create_user_with_role_grant(program, UserRole.STAFF, user)

        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)
                self.assertEqual(response_data["filters"], [])

    def test_finalist_user_gets_all_programs_in_program_group(self):
        named_group = NamedGroupFactory()
        programs = ProgramFactory.create_batch(
            5,
            mentor_program_group=named_group,
            program_status=ACTIVE_PROGRAM_STATUS)
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
        programs = ProgramFactory.create_batch(
            5,
            mentor_program_group=named_group,
            program_status=ACTIVE_PROGRAM_STATUS)
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

    def test_alumni_user_only_sees_mentors_of_alumni_programs(self):
        named_group = NamedGroupFactory()
        named_alumni_group = NamedGroupFactory()
        programs = ProgramFactory.create_batch(
            5,
            mentor_program_group=named_group,
            program_status=ENDED_PROGRAM_STATUS)
        alumni_program = ProgramFactory(
                                program_status=ACTIVE_PROGRAM_STATUS,
                                mentor_program_group=named_alumni_group)
        finalist_program = programs[0]

        user = self._create_user_with_role_grant(
            finalist_program, UserRole.FINALIST)
        self._create_user_with_role_grant(
            alumni_program, UserRole.ALUM, user)

        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)

                for program in programs:
                    self.assertNotIn(program.name, response_data["filters"])
                self.assertIn(alumni_program.name, response_data["filters"])

    def test_alumni_user_who_is_also_finalist_sees_mentors_of_both_programs(
            self):
        named_group = NamedGroupFactory()
        named_alumni_group = NamedGroupFactory()
        programs = ProgramFactory.create_batch(
            5,
            mentor_program_group=named_group,
            program_status=ACTIVE_PROGRAM_STATUS)
        other_program = ProgramFactory(program_status=ACTIVE_PROGRAM_STATUS,
                                       mentor_program_group=named_alumni_group)

        finalist_program = programs[1]

        user = self._create_user_with_role_grant(
            other_program, UserRole.ALUM)
        self._create_user_with_role_grant(
            finalist_program, UserRole.FINALIST, user)

        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)

                for program in programs:
                    self.assertIn(program.name, response_data["filters"])
                self.assertIn(other_program.name, response_data["filters"])

    def test_superuser_employee_sees_all_mentors(self):
        user = self._create_expert()
        user.is_superuser = True
        user.save()

        with self.settings(
                ALGOLIA_APPLICATION_ID='test',
                ALGOLIA_API_KEY='test'):
            with self.login(email=user.email):
                response = self.client.get(self.url)
                response_data = json.loads(response.content)

                self.assertEqual(response_data["filters"], [])

    def _create_entrepreneur(self):
        ent_user = EntrepreneurFactory()
        ent_user.set_password("password")
        ent_user.save()
        return ent_user

    def _create_expert(self):
        expert_user = ExpertFactory()
        expert_user.set_password("password")
        expert_user.save()
        return expert_user

    def _create_user_with_role_grant(
            self, program, user_role_name, user=False):
        user_role = UserRoleFactory(name=user_role_name)
        program_role = ProgramRoleFactory(
            user_role=user_role,
            program=program
        )

        if not user:
            user = self._create_entrepreneur()

        ProgramRoleGrantFactory(person=user, program_role=program_role)
        return user
