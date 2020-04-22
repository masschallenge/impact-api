from unittest.mock import patch

from django.urls import reverse

from accelerator.tests.contexts.context_utils import get_user_role_by_name
from accelerator.models import UserRole
from accelerator.tests.factories import (
    ProgramFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
    UserFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.v1.views import UserProgramConfirmationDetailView
from impact.v1.views.user_program_confirmation_detail_view import INVALID_INPUT_ERROR

IMPACT_BACKEND_PATH = 'impact.impact_email_backend.ImpactEmailBackend'


class TestUserConfirmParticipationView(APITestCase):
    def setUp(self):
        self.program = ProgramFactory()
        ProgramRoleFactory(
            user_role=get_user_role_by_name(UserRole.MENTOR),
            program=self.program
        )
        ProgramRoleFactory(
            user_role=get_user_role_by_name(UserRole.DEFERRED_MENTOR),
            program=self.program
        )

    def test_user_get_program_participation_status(self):
        user = self.basic_user()
        deferred_program = _get_programrolegrant_for_role(
            UserRole.DEFERRED_MENTOR, user).program_role.program
        confirmed_program = _get_programrolegrant_for_role(
            UserRole.MENTOR, user).program_role.program
        with self.login(email=user.email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[user.pk])
            response = self.client.get(url)
            expected = {
                'confirmed': [confirmed_program.pk],
                'deferred': [deferred_program.pk],
            }
            self.assertEqual(response.data['program_confirmation'], expected)

    def test_user_post_confirmed_participation(self):
        user = self.basic_user()
        with self.login(email=user.email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[user.pk])
            self.client.post(url, {
                'confirmed': [self.program.pk, ],
            })
            expected = _get_user_programs_for_role(
                user, UserRole.MENTOR)
            self.assertIn(self.program.pk, expected)

    def test_user_post_deferred_participation(self):
        user = self.basic_user()
        with self.login(email=user.email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[user.pk])
            self.client.post(url, {
                'deferred': [self.program.pk],
            })
            expected = _get_user_programs_for_role(
                user, UserRole.DEFERRED_MENTOR)
            self.assertIn(self.program.pk, expected)

    def test_confirming_program_removes_deferred_status(self):
        user = self.basic_user()
        _get_programrolegrant_for_role(
            UserRole.DEFERRED_MENTOR, user, self.program)
        with self.login(email=user.email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[user.pk])
            self.client.post(url, {
                'confirmed': [self.program.pk],
            })
            response = self.client.get(url)
            expected = {
                'deferred': [],
                'confirmed': [self.program.pk]
            }
            self.assertEqual(response.data['program_confirmation'], expected)

    def test_deferring_program_removes_confirmed_status(self):
        user = self.basic_user()
        _get_programrolegrant_for_role(
            UserRole.MENTOR, user, self.program)
        with self.login(email=user.email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[user.pk])
            self.client.post(url, {
                'deferred': [self.program.pk],
            })
            response = self.client.get(url)
            expected = {
                'deferred': [self.program.pk],
                'confirmed': []
            }
            self.assertEqual(response.data['program_confirmation'], expected)

    def test_only_owner_can_access_participation_view(self):
        non_owner_user = UserFactory()
        with self.login(email=self.basic_user_without_api_groups().email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[non_owner_user.pk])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)

    def test_cannot_post_invalid_input(self):
        user = self.basic_user()
        with self.login(email=user.email):
            url = reverse(UserProgramConfirmationDetailView.view_name,
                          args=[user.pk])
            response = self.client.post(url, {
                'deferred': ["test"],
            })
            expected = {
                'detail': INVALID_INPUT_ERROR.format('deferred'),
            }
            self.assertEqual(response.data, expected)

    @patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
    def test_email_is_sent_after_confirming_participation(
            self,
            mocked_backend):
        user = self.basic_user()
        with self.settings(
                EMAIL_BACKEND=IMPACT_BACKEND_PATH):
            with self.login(email=user.email):
                url = reverse(UserProgramConfirmationDetailView.view_name,
                              args=[user.pk])
                self.client.post(url, {
                    'confirmed': [self.program.pk],
                })
            self.assertTrue(mocked_backend.called)


def _get_user_programs_for_role(user, role):
    return list(
        user.programrolegrant_set.filter(
            program_role__user_role__name=role,
        ).values_list('program_role__program', flat=True).distinct())


def _get_programrolegrant_for_role(role, user, program=None):
    return ProgramRoleGrantFactory(
        person=user,
        program_role__program=program or ProgramFactory(),
        program_role__user_role=get_user_role_by_name(role))
