from django.urls import reverse

from .api_test_case import APITestCase
from ..v1.views import ReserveOfficeHourView
from ..permissions.v1_api_permissions import DEFAULT_PERMISSION_DENIED_DETAIL
from .factories import UserFactory
from .utils import nonexistent_object_id
from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
    StartupFactory,
    StartupTeamMemberFactory,
)
from accelerator.tests.contexts import UserRoleContext
from accelerator.models import UserRole


class TestReserveOfficeHourView(APITestCase):
    view = ReserveOfficeHourView
    success_header = ReserveOfficeHourView.SUCCESS_HEADER
    fail_header = ReserveOfficeHourView.FAIL_HEADER

    def test_finalist_reserves_office_hour_success(self):
        # a finalist reserves an office hour, gets success response
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      request_user=finalist)
        self.assert_ui_notification(response, True, self.view.SUCCESS_DETAIL)

    def test_finalist_reserves_unspecified_office_hour(self):
        # a finalist reserves an office hour, gets success response
        finalist = _finalist()
        response = self.post_response("",
                                      request_user=finalist)
        self.assert_ui_notification(response,
                                    False,
                                    self.view.NO_OFFICE_HOUR_SPECIFIED)

    def test_finalist_reserves_office_hour_timecard(self):
        # a finalist reserves an office hour, gets timecard details in response
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        stm = StartupTeamMemberFactory(user=finalist)

        response = self.post_response(office_hour.id,
                                      startup_id=stm.startup.id,
                                      request_user=finalist)
        self.assert_response_contains_session_details(response, office_hour)

    def test_finalist_reserves_office_hour_with_nonexistent_startup(self):
        # a finalist reserves an office hour, gets timecard details in response
        startup_id = nonexistent_object_id(StartupFactory)
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      startup_id=startup_id,
                                      request_user=finalist)
        self.assert_ui_notification(response,
                                    False,
                                    self.view.NO_SUCH_STARTUP)

    def test_non_finalist_attempts_to_reserve_office_hour_notification(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        non_finalist = self.basic_user()
        response = self.post_response(office_hour.id,
                                      request_user=non_finalist)
        self.assert_ui_notification(response,
                                    False,
                                    self.view.USER_CANNOT_RESERVE_OFFICE_HOURS)

    def test_non_finalist_attempts_to_reserve_office_hour_and_fails(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        non_finalist = self.basic_user()
        self.post_response(office_hour.id,
                                      request_user=non_finalist)
        self.assert_not_reserved(office_hour)

    def test_finalist_reserves_office_hour_gets_confirmation_email(self):
        # a finalist reserves and office hour, gets a confirmation email
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        self.post_response(office_hour.id,
                           request_user=finalist)
        self.assert_notified(finalist)

    def test_previously_reserved_office_hour_gets_failure(self):
        # a finalist reserves a reserved office hour, gets failure response
        office_hour = MentorProgramOfficeHourFactory()
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      request_user=finalist)
        self.assert_ui_notification(response,
                                    False,
                                    self.view.OFFICE_HOUR_ALREADY_RESERVED)

    def test_reserve_on_behalf_of_success(self):
        # staff reserves a session on behalf of finalist, gets success
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      finalist.id)
        self.assert_ui_notification(response, True, self.view.SUCCESS_DETAIL)

    def test_reserve_on_behalf_of_nonexistent_user(self):
        # staff reserves a session on behalf of finalist, gets success
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist_id = nonexistent_object_id(UserFactory)
        response = self.post_response(office_hour.id,
                                      finalist_id)
        self.assert_ui_notification(response, False, self.view.NO_SUCH_USER)

    def test_nonexistent_office_hour(self):
        # staff reserves a session on behalf of finalist, gets success
        office_hour_id = nonexistent_object_id(MentorProgramOfficeHourFactory)
        finalist = _finalist()
        response = self.post_response(office_hour_id,
                                      finalist.id)
        self.assert_ui_notification(response,
                                    False,
                                    self.view.NO_SUCH_OFFICE_HOUR)

    def test_reserve_on_behalf_of_finalist_gets_email_notification(self):
        # staff reserves a session on behalf of finalist, finalist is
        # notified by email
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        self.post_response(office_hour.id,
                           finalist.id)
        self.assert_notified(finalist)

    def test_reserve_on_behalf_of_mentor_gets_email_notification(self):
        # staff reserves a session on behalf of finalist, mentor is
        # notified by email
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        self.post_response(office_hour.id,
                           finalist.id)
        self.assert_notified(office_hour.mentor)

    def test_non_staff_reserve_on_behalf_of_failure(self):
        # finalist reserves a session on behalf of finalist, gets failure
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      finalist.id,
                                      request_user=_finalist())
        self.assert_ui_notification(response,
                                    False,
                                    DEFAULT_PERMISSION_DENIED_DETAIL)

    def assert_response_contains_session_details(self, response, office_hour):
        office_hour.refresh_from_db()
        timecard = response.data['timecard_info']
        if office_hour.startup:
            startup_name = office_hour.startup.organization.name
        else:
            startup_name = ""
        oh_details = {'finalist_first_name': office_hour.finalist.first_name,
                      'finalist_last_name': office_hour.finalist.last_name,
                      'topics': office_hour.description,
                      'startup': startup_name}
        self.assertDictEqual(timecard, oh_details)

    def assert_reserved_by(self, office_hour, finalist):
        office_hour.refresh_from_db()
        self.assertEqual(office_hour.finalist, finalist)

    def assert_not_reserved_by(self, office_hour, finalist):
        office_hour.refresh_from_db()
        self.assertNotEqual(office_hour.finalist, finalist)

    def assert_not_reserved(self, office_hour):
        office_hour.refresh_from_db()
        self.assertIsNone(office_hour.finalist)

    def post_response(self,
                      office_hour_id,
                      user_id=None,
                      startup_id=None,
                      request_user=None):
        request_user = request_user or self.staff_user()

        request_user.set_password("password")
        request_user.save()
        url = reverse(self.view.view_name)
        data = {}
        if office_hour_id:
            data['office_hour_id'] = office_hour_id
        if user_id:
            data['user_id'] = user_id
        if startup_id:
            data['startup_id'] = startup_id
        with self.login(request_user):
            return self.post(url, data=data)


def _finalist():
    return UserRoleContext(UserRole.FINALIST).user


def _mentor():
    return UserRoleContext(UserRole.MENTOR).user
