from datetime import datetime, timedelta
from django.core import mail
from django.urls import reverse

from accelerator.models import MentorProgramOfficeHour, UserRole
from accelerator.tests.contexts import UserRoleContext
from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
    ProgramFactory
)
from accelerator.tests.factories.location_factory import LocationFactory

from impact.permissions.v1_api_permissions import (
    DEFAULT_PERMISSION_DENIED_DETAIL,
)
from impact.tests.api_test_case import APITestCase
from impact.v1.serializers.office_hours import INVALID_END_DATE
from impact.v1.views.office_hour_view import (
    FAIL_CREATE_HEADER,
    FAIL_EDIT_HEADER,
    SUCCESS_CREATE_HEADER,
    SUCCESS_EDIT_HEADER,
    OfficeHourViewSet
)


class TestCreateEditOfficeHourView(APITestCase):
    url = reverse(f'{OfficeHourViewSet.view_name}-list')

    def test_mentor_can_create_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        self._assert_office_hour_created(mentor)

    def test_mentor_can_create_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        self._assert_office_hour_created(mentor, from_now=-120)

    def test_mentor_can_create_office_hour_session_response_details(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(mentor, data)
        self._assert_success_response(response.data)

    def test_mentor_can_edit_own_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        self._assert_update_office_hour(mentor, office_hour)

    def test_mentor_can_edit_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor, from_now=-120)
        self._assert_update_office_hour(mentor, office_hour)

    def test_mentor_can_edit_office_hour_session_response_details(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(mentor, data)
        self._assert_success_response(response.data)

    def test_staff_can_create_office_hour_session_on_behalf_of_mentor(self):
        mentor = self._expert_user(UserRole.MENTOR)
        self._assert_office_hour_created(mentor, staff=True)

    def test_staff_can_create_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        self._assert_office_hour_created(mentor, from_now=-120, staff=True)

    def test_staff_can_create_office_hour_on_behalf_of_mentor_response(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(self.staff_user(), data)
        self._assert_success_response(response.data)

    def test_staff_can_edit_office_hour_session_on_behalf_of_mentor(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        self._assert_update_office_hour(mentor, office_hour, staff=True)

    def test_staff_can_edit_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor, from_now=-120)
        self._assert_update_office_hour(mentor, office_hour, staff=True)

    def test_mail_to_mentor_when_staff_create_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        self._create_office_hour_session(self.staff_user(), data)
        self.assertEqual(mail.outbox[0].to, [mentor.email])

    def test_mail_to_mentor_when_staff_updates_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        data = self._get_patch_request_data(office_hour, {
            'topics': 'Updated topics',
            'description': 'Updated description', })
        self._edit_office_hour_session(self.staff_user(), office_hour, data)
        self.assertEqual(mail.outbox[0].to, [mentor.email])

    def test_mentor_not_in_active_program_cannot_create_office_hour(self):
        mentor = self._expert_with_inactive_program(UserRole.MENTOR)
        self._assert_office_hour_was_not_created(mentor)

    def test_mentor_in_non_active_program_cant_create_office_response(self):
        mentor = self._expert_with_inactive_program(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(mentor, data)
        self.assertEqual(response.data['detail'],
                         DEFAULT_PERMISSION_DENIED_DETAIL)

    def test_office_hour_start_date_must_be_later_than_start_date(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = datetime.now()
        data = self._get_post_request_data(mentor, get_data={
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=-30),
        })
        response = self._create_office_hour_session(mentor, data)
        self.assertIn(INVALID_END_DATE,
                      response.data['errors']['end_date_time'])

    def test_none_staff_or_none_mentor_response(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(self.basic_user(), data)
        self.assertEqual(response.data['detail'],
                         DEFAULT_PERMISSION_DENIED_DETAIL)

    def test_use_request_user_for_mentor_users(self):
        mentor = self._expert_user(UserRole.MENTOR)
        mentor2 = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor,
                                           get_data={'mentor': mentor2.id})
        response = self._create_office_hour_session(mentor, data)
        self.assertEqual(response.data['data']['mentor']['id'], mentor.id)

    def _expert_with_inactive_program(self, role):
        program = ProgramFactory(program_status='ended')
        return self._expert_user(role, program)

    def _get_post_request_data(self, mentor, from_now=0, get_data=None):
        location = LocationFactory()
        start_time = datetime.now() + timedelta(minutes=from_now)
        data = {
            'mentor': mentor.id,
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=30),
            'topics': 'topics',
            'description': 'description',
            'location': location.id
        }
        if get_data:
            data.update(get_data)
        return data

    def _get_patch_request_data(self, office_hour, patch_data=None):
        data = {
            'mentor': office_hour.mentor.id,
            'start_date_time': office_hour.start_date_time,
            'end_date_time': office_hour.end_date_time,
            'topics': office_hour.topics,
            'description': office_hour.description,
            'location': office_hour.location.id
        }
        if patch_data:
            data.update(patch_data)
        return data

    def _assert_success_response(self, data, edit=False):
        header = SUCCESS_EDIT_HEADER if edit else SUCCESS_CREATE_HEADER
        self.assertTrue(all([
            data['success'],
            data['header'] == header,
        ]))

    def _assert_fail_response(self, data, edit=False):
        header = FAIL_EDIT_HEADER if edit else FAIL_CREATE_HEADER
        self.assertTrue(all([
            not data['success'],
            data['header'] == header,
        ]))

    def _office_hour_created(self, mentor, from_now, staff):
        count_before = MentorProgramOfficeHour.objects.count()
        data = self._get_post_request_data(mentor, from_now)
        user = self.staff_user() if staff else mentor
        self._create_office_hour_session(user, data)
        count_after = MentorProgramOfficeHour.objects.count()
        return count_after == count_before + 1

    def _assert_office_hour_created(self, mentor, from_now=30, staff=False):
        self.assertTrue(self._office_hour_created(mentor, from_now, staff))

    def _assert_office_hour_was_not_created(self, mentor,
                                            from_now=30, staff=False):
        self.assertFalse(self._office_hour_created(mentor, from_now, staff))

    def _create_office_hour_obj(self, mentor, from_now=0, finalist=None):
        start_time = datetime.now() + timedelta(minutes=from_now)
        end_time = start_time + timedelta(minutes=30)
        return MentorProgramOfficeHourFactory(
            mentor=mentor,
            start_date_time=start_time,
            end_date_time=end_time,
            finalist=finalist,
        )

    def _assert_update_office_hour(self, mentor, office_hour, staff=False):
        updated_topics = 'updated topics'
        data = self._get_patch_request_data(office_hour,
                                            {'topics': updated_topics})
        user = self.staff_user() if staff else mentor
        self._edit_office_hour_session(user, office_hour, data)
        updated_office_hour = MentorProgramOfficeHour.objects.get(
            pk=office_hour.id)
        self.assertEqual(updated_office_hour.topics, updated_topics)

    def _create_office_hour_session(self, user, data):
        with self.login(email=user.email):
            return self.client.post(self.url, data)

    def _edit_office_hour_session(self, user, office_hour, data):
        with self.login(email=user.email):
            url = '{}{}/'.format(self.url, office_hour.id)
            return self.client.patch(url, data)

    def _expert_user(self, role, program=None):
        user = UserRoleContext(
            user_role_name=role,
            program=program).user
        user.set_password('password')
        user.save()
        return user
