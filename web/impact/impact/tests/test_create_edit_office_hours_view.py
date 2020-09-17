from contextlib import contextmanager
from datetime import (
    datetime,
    timedelta,
)
from pytz import (
    timezone,
    utc,
)

from django.core import mail
from django.urls import reverse

from accelerator.tests.contexts import UserRoleContext
from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
    ProgramFactory,
)
from accelerator.tests.factories.location_factory import LocationFactory
from accelerator_abstract.models.base_clearance import (
    CLEARANCE_LEVEL_EXEC_MD,
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    CLEARANCE_LEVEL_POM,
    CLEARANCE_LEVEL_STAFF,
)
from ..permissions.v1_api_permissions import CREATE_PERMISSION_DENIED_DETAIL
from ..v1.serializers.office_hours_serializer import (
    CONFLICTING_SESSIONS,
    INVALID_END_DATE,
    INVALID_SESSION_DURATION,
    INVALID_USER,
)
from ..v1.views.office_hour_view import (
    FAIL_CREATE_HEADER,
    FAIL_EDIT_HEADER,
    SUCCESS_CREATE_HEADER,
    SUCCESS_EDIT_HEADER,
    OfficeHourViewSet,
)
from ..v1.views.utils import HOUR_MINUTE_FORMAT
from .api_test_case import APITestCase
from mc.utils import swapper_model
Location = swapper_model('Location')
MentorProgramOfficeHour = swapper_model('MentorProgramOfficeHour')
UserRole = swapper_model('UserRole')


class TestCreateEditOfficeHourView(APITestCase):
    url = reverse(f'{OfficeHourViewSet.view_name}-list')
    updated_topics = 'updated topics'

    def test_mentor_can_create_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        with self._assert_office_hour_created():
            self._create_office_hour_session(mentor, data)

    def test_mentor_can_create_multi_session_office_hour_block(self):
        mentor = self._expert_user(UserRole.MENTOR)
        now = _now()
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': now,
                      'end_date_time': now + timedelta(hours=2)})
        with self._assert_office_hour_created(count=4):
            self._create_office_hour_session(mentor, data)

    def test_mentor_cannot_create_short_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        now = _now()
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': now,
                      'end_date_time': now + timedelta(minutes=20)})
        with self._assert_office_hour_created(created=False):
            self._create_office_hour_session(mentor, data)

    def test_mentor_cannot_create_short_session_ui(self):
        mentor = self._expert_user(UserRole.MENTOR)
        now = _now()
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': now,
                      'end_date_time': now + timedelta(minutes=20)})
        response = self._create_office_hour_session(mentor, data)
        self._assert_error_response(response,
                                    key='end_date_time',
                                    expected=INVALID_SESSION_DURATION)

    def test_mentor_can_create_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor, minutes_from_now=-120)
        with self._assert_office_hour_created():
            self._create_office_hour_session(mentor, data)

    def test_mentor_can_create_office_hour_session_response_details(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(mentor, data)
        self._assert_success_response(response)

    def test_mentor_can_edit_own_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        data = {'topics': self.updated_topics}
        self._edit_office_hour_session(mentor, office_hour, data)
        self._assert_update_office_hour(office_hour)

    def test_mentor_cannot_edit_office_hour_session_to_end_before_start(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        bad_end_date_time = office_hour.start_date_time - timedelta(minutes=30)
        data = {
            "start_date_time": office_hour.start_date_time,
            "end_date_time": bad_end_date_time}
        response = self._edit_office_hour_session(mentor, office_hour, data)
        self._assert_error_response(response,
                                    key="end_date_time",
                                    expected=INVALID_END_DATE)

    def test_mentor_can_edit_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor,
                                                   minutes_from_now=-120)
        data = {'topics': self.updated_topics}
        self._edit_office_hour_session(mentor, office_hour, data)
        self._assert_update_office_hour(office_hour)

    def test_mentor_can_edit_office_hour_session_response_details(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(mentor, data)
        self._assert_success_response(response)

    def test_staff_can_create_office_hour_session_on_behalf_of_mentor(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        with self._assert_office_hour_created():
            self._create_office_hour_session(self.staff_user(), data)

    def test_staff_can_create_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor, minutes_from_now=-120)
        with self._assert_office_hour_created():
            self._create_office_hour_session(self.staff_user(), data)

    def test_staff_can_create_office_hour_on_behalf_of_mentor_response(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(self.staff_user(), data)
        self._assert_success_response(response)

    def test_staff_can_edit_office_hour_session_on_behalf_of_mentor(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        data = {'topics': self.updated_topics}
        self._edit_office_hour_session(self.staff_user(), office_hour, data)
        self._assert_update_office_hour(office_hour)

    def test_staff_can_edit_office_hour_session_for_date_prior_to_now(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor,
                                                   minutes_from_now=-120)
        data = {'topics': self.updated_topics}
        self._edit_office_hour_session(self.staff_user(), office_hour, data)
        self._assert_update_office_hour(office_hour)

    def test_mail_to_mentor_when_staff_create_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        self._create_office_hour_session(self.staff_user(), data)
        self.assert_notified(mentor)

    def test_mail_to_mentor_when_staff_updates_office_hour_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        data = {'topics': self.updated_topics}
        self._edit_office_hour_session(self.staff_user(), office_hour, data)
        self.assert_notified(mentor)

    def test_mentor_not_in_active_program_cannot_create_office_hour(self):
        mentor = self._expert_with_inactive_program(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        with self._assert_office_hour_created(created=False):
            self._create_office_hour_session(mentor, data)

    def test_mentor_in_non_active_program_cant_create_office_response(self):
        mentor = self._expert_with_inactive_program(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(mentor, data)
        self.assertEqual(response.data['detail'],
                         CREATE_PERMISSION_DENIED_DETAIL)

    def test_office_hour_end_date_must_be_later_than_start_date(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = datetime.now()
        data = self._get_post_request_data(mentor, get_data={
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=-30)})
        response = self._create_office_hour_session(mentor, data)
        self._assert_error_response(response,
                                    key='end_date_time',
                                    expected=INVALID_END_DATE)

    def test_none_staff_or_none_mentor_response(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor)
        response = self._create_office_hour_session(self.basic_user(), data)
        self.assertEqual(response.data['detail'],
                         CREATE_PERMISSION_DENIED_DETAIL)

    def test_use_request_user_for_mentor_users(self):
        mentor = self._expert_user(UserRole.MENTOR)
        mentor2 = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor,
                                           get_data={'mentor': mentor2.id})
        response = self._create_office_hour_session(mentor, data)
        self.assertEqual(response.data['data'][0]['mentor']['id'], mentor.id)

    def test_admin_cant_create_office_hour_for_non_mentor_user_response(self):
        user = self._expert_user(UserRole.JUDGE)
        data = self._get_post_request_data(user)
        response = self._create_office_hour_session(self.staff_user(), data)
        self._assert_error_response(response,
                                    key='mentor', expected=INVALID_USER)

    def test_admin_cant_create_office_hour_for_non_mentor_user(self):
        user = self._expert_user(UserRole.JUDGE)
        data = self._get_post_request_data(user)
        with self._assert_office_hour_created(created=False):
            self._create_office_hour_session(self.staff_user(), data)

    def test_mentor_cant_create_conflicting_sessions(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(mentor, start_date_time=start_time)
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': start_time,
                      'end_date_time': start_time + timedelta(hours=2)})
        with self._assert_office_hour_created(created=False):
            self._create_office_hour_session(mentor, data)

    def test_mentor_cant_create_conflicting_sessions_response(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(mentor, start_date_time=start_time)
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': start_time,
                      'end_date_time': start_time + timedelta(hours=2)})
        response = self._create_office_hour_session(mentor, data)
        self._assert_error_response(response,
                                    key='start_date_time',
                                    expected=CONFLICTING_SESSIONS)

    def test_mentor_cant_update_session_to_start_at_conflicting_time(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(mentor, start_date_time=start_time)
        office_hour = self._create_office_hour_obj(mentor)
        data = {
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=30)}
        self._edit_office_hour_session(mentor, office_hour, data)
        self._assert_office_hour_not_updated(office_hour)

    def test_can_create_sessions_sharing_start_time_boundaries(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(mentor, start_date_time=start_time)
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': start_time + timedelta(minutes=-30),
                      'end_date_time': start_time})
        with self._assert_office_hour_created(created=True):
            self._create_office_hour_session(mentor, data)

    def test_can_create_sessions_sharing_end_time_boundaries(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(mentor, start_date_time=start_time)
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': start_time + timedelta(minutes=30),
                      'end_date_time': start_time + timedelta(minutes=60)})
        with self._assert_office_hour_created(created=True):
            self._create_office_hour_session(mentor, data)

    def test_cant_create_session_when_conflict_exists_in_the_block(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(
            mentor, start_date_time=start_time, block_duration=120)
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': start_time + timedelta(minutes=60),
                      'end_date_time': start_time + timedelta(minutes=150)})
        with self._assert_office_hour_created(count=0):
            self._create_office_hour_session(mentor, data)

    def test_cant_create_session_with_enclosing_conflict(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(
            mentor, start_date_time=start_time, block_duration=120)
        data = self._get_post_request_data(
            mentor,
            get_data={'start_date_time': start_time + timedelta(minutes=60),
                      'end_date_time': start_time + timedelta(minutes=90)})
        with self._assert_office_hour_created(count=0):
            self._create_office_hour_session(mentor, data)

    def test_mentor_cant_update_session_with_enclosing_conflicts(self):
        mentor = self._expert_user(UserRole.MENTOR)
        start_time = _now()
        self._create_office_hour_obj(
            mentor,
            start_date_time=start_time + timedelta(minutes=-30),
            block_duration=120)
        office_hour = self._create_office_hour_obj(mentor)
        data = {
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=30)}
        self._edit_office_hour_session(mentor, office_hour, data)
        self._assert_office_hour_not_updated(office_hour)

    def test_user_with_staff_clearance_can_create_office_hours(self):
        self.assert_user_with_clearance_can_create_office_hours(
            CLEARANCE_LEVEL_STAFF)

    def test_user_with_pom_clearance_can_create_office_hours(self):
        self.assert_user_with_clearance_can_create_office_hours(
            CLEARANCE_LEVEL_POM)

    def test_user_with_exec_md_clearance_can_create_office_hours(self):
        self.assert_user_with_clearance_can_create_office_hours(
            CLEARANCE_LEVEL_EXEC_MD)

    def test_global_manager_can_create_office_hours(self):
        self.assert_user_with_clearance_can_create_office_hours(
            CLEARANCE_LEVEL_GLOBAL_MANAGER)

    def test_create_office_hour_block_mail_has_correct_time(self):
        mentor = self._expert_user(UserRole.MENTOR)
        data = self._get_post_request_data(mentor, block_duration=120)
        self._create_office_hour_session(self.staff_user(), data)
        tz = Location.objects.get(pk=int(data['location'])).timezone
        self._assert_mail_has_correct_session_time(data, tz)

    def test_edit_office_hour_session_mail_has_correct_time(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = self._create_office_hour_obj(mentor)
        tz = office_hour.location.timezone
        start_time = _now() + timedelta(minutes=60)
        data = {
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=30),
        }
        self._edit_office_hour_session(self.staff_user(), office_hour, data)
        self._assert_mail_has_correct_session_time(data, tz)

    def _expert_with_inactive_program(self, role):
        program = ProgramFactory(program_status='ended')
        return self._expert_user(role, program)

    def _get_post_request_data(self,
                               mentor,
                               minutes_from_now=0,
                               get_data=None,
                               block_duration=30):
        location = LocationFactory()
        start_time = _now() + timedelta(minutes=minutes_from_now)
        data = {
            'mentor': mentor.id,
            'start_date_time': start_time,
            'end_date_time': start_time + timedelta(minutes=block_duration),
            'topics': 'topics',
            'description': 'description',
            'location': location.id
        }
        if get_data:
            data.update(get_data)
        return data

    def assert_user_with_clearance_can_create_office_hours(
            self, clearance_level):
        program_family = ProgramFactory().program_family
        staff_user = self.staff_user(program_family=program_family,
                                     level=clearance_level)
        data = self._get_post_request_data(staff_user)
        with self._assert_office_hour_created():
            self._create_office_hour_session(staff_user, data)

    def _assert_success_response(self, response, edit=False):
        header = SUCCESS_EDIT_HEADER if edit else SUCCESS_CREATE_HEADER
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['header'], header)

    def _assert_fail_response(self, response, edit=False):
        header = FAIL_EDIT_HEADER if edit else FAIL_CREATE_HEADER
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['header'], header)

    def _assert_error_response(self, response, key, expected):
        self.assertIn(expected, response.data['errors'][key])

    def _create_office_hour_obj(self,
                                mentor,
                                minutes_from_now=0,
                                finalist=None,
                                start_date_time=None,
                                block_duration=30,
                                ):
        start_time = start_date_time or _now() + timedelta(
            minutes=minutes_from_now)
        end_time = start_time + timedelta(minutes=block_duration)
        return MentorProgramOfficeHourFactory(
            mentor=mentor,
            start_date_time=start_time,
            end_date_time=end_time,
            finalist=finalist,
        )

    def _assert_update_office_hour(self, office_hour):
        updated_office_hour = MentorProgramOfficeHour.objects.get(
            pk=office_hour.id)
        self.assertEqual(updated_office_hour.topics, self.updated_topics)

    def _assert_office_hour_not_updated(self, office_hour):
        previously_updated_at = office_hour.updated_at
        office_hour.refresh_from_db()
        self.assertEqual(previously_updated_at, office_hour.updated_at)

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

    @contextmanager
    def _assert_office_hour_created(self, created=True, count=1):
        count_before = MentorProgramOfficeHour.objects.count()
        yield
        count_after = MentorProgramOfficeHour.objects.count()
        if not created:
            self.assertEqual(count_after, count_before)
        else:
            self.assertEqual(count_after, count_before + count)

    def _assert_mail_has_correct_session_time(self, data, tz):
        start_time = _localized_time(data['start_date_time'], tz)
        end_time = _localized_time(data['end_date_time'], tz)
        expected_start_time = start_time.strftime(HOUR_MINUTE_FORMAT)
        expected_end_time = end_time.strftime(HOUR_MINUTE_FORMAT)
        expected_time = f"{expected_start_time}-{expected_end_time}"
        self.assertIn(expected_time, mail.outbox[0].body)


def _localized_time(time, tz):
    return time.astimezone(timezone(tz))


def _now():
    return utc.localize(datetime.utcnow())
