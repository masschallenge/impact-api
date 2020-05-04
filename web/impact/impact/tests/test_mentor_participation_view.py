from django.core import mail
from django.urls import reverse

from accelerator.tests.contexts.context_utils import get_user_role_by_name
from accelerator.models import UserRole
from accelerator.tests.factories import (
    ProgramFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.tests.test_graphql import expert_user
from impact.v1.views import MentorParticipationView
from impact.v1.views.mentor_participation_view import (
    INVALID_INPUT_ERROR,
    SUBJECT
)


class TestMentorParticipationView(APITestCase):
    url = reverse(MentorParticipationView.view_name)

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

    def test_expert_post_confirmed_participation(self):
        user = expert_user()
        with self.login(email=user.email):
            self.client.post(self.url, {
                'confirmed': [self.program.pk, ],
            })
            expected = _get_user_programs_for_role(
                user, UserRole.MENTOR)
            self.assertIn(self.program.pk, expected)

    def test_user_post_deferred_participation(self):
        user = expert_user()
        with self.login(email=user.email):
            self.client.post(self.url, {
                'deferred': [self.program.pk],
            })
            expected = _get_user_programs_for_role(
                user, UserRole.DEFERRED_MENTOR)
            self.assertIn(self.program.pk, expected)

    def test_confirming_program_removes_deferred_status(self):
        user = expert_user()
        _create_program_role_grant_for_role(
            UserRole.DEFERRED_MENTOR, user, self.program)
        with self.login(email=user.email):
            self.client.post(self.url, {
                'confirmed': [self.program.pk],
            })
            deferred_count = user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.DEFERRED_MENTOR,
            ).count()
            self.assertEqual(deferred_count, 0)

    def test_deferring_program_removes_confirmed_status(self):
        user = expert_user()
        _create_program_role_grant_for_role(
            UserRole.MENTOR, user, self.program)
        with self.login(email=user.email):
            self.client.post(self.url, {
                'deferred': [self.program.pk],
            })
            confirmed_count = user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.MENTOR,
            ).count()
            self.assertEqual(confirmed_count, 0)

    def test_cannot_post_invalid_input(self):
        user = expert_user()
        with self.login(email=user.email):
            response = self.client.post(self.url, {
                'deferred': ["test"],
            })
            expected = {
                'detail': INVALID_INPUT_ERROR.format('deferred'),
            }
            self.assertEqual(response.data, expected)

    def test_email_is_sent_after_confirming_participation(self):
        user = expert_user()
        with self.login(email=user.email):
            self.client.post(self.url, {
                'confirmed': [self.program.pk],
            })
        self.assertEqual(mail.outbox[0].subject, SUBJECT)

    def test_non_expert_cannot_post_participation(self):
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, {
                'deferred': [0],
            })
            expected = {
                'detail': 'You do not have permission to perform this action.',
            }
            self.assertEqual(response.data, expected)


def _get_user_programs_for_role(user, role):
    return list(
        user.programrolegrant_set.filter(
            program_role__user_role__name=role,
        ).values_list('program_role__program', flat=True).distinct())


def _create_program_role_grant_for_role(role, user, program=None):
    return ProgramRoleGrantFactory(
        person=user,
        program_role__program=program or ProgramFactory(),
        program_role__user_role=get_user_role_by_name(role))
