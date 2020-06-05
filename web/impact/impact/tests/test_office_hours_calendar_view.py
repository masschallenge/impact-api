from datetime import (
    datetime,
    timedelta,
)
from pytz import utc

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from accelerator.models import UserRole
from accelerator.tests.factories.location_factory import LocationFactory
from accelerator.tests.factories.program_family_location_factory import (
    ProgramFamilyLocationFactory,
)
from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
    ProgramFamilyFactory,
    ProgramRoleGrantFactory,
)
from accelerator.tests.contexts.context_utils import get_user_role_by_name
from accelerator.tests.utils import days_from_now

from impact.tests.api_test_case import APITestCase
from impact.tests.factories import UserFactory
from impact.v1.views import (
    ISO_8601_DATE_FORMAT,
    OfficeHoursCalendarView,
)


class TestOfficeHoursCalendarView(APITestCase):
    view = OfficeHoursCalendarView

    def test_no_date_specified_sees_current_week(self):
        office_hour = self.create_office_hour()
        response = self.get_response(user=office_hour.mentor)
        self.assert_hour_in_response(response, office_hour)

    def test_no_date_specified_does_not_see_last_week(self):
        office_hour = self.create_office_hour(
            start_date_time=days_from_now(-9))
        response = self.get_response(user=office_hour.mentor)
        self.assert_hour_not_in_response(response, office_hour)

    def test_date_specified_sees_sessions_in_range(self):
        two_weeks_ago = days_from_now(-14)
        date_spec = two_weeks_ago.strftime(ISO_8601_DATE_FORMAT)
        office_hour = self.create_office_hour(
            start_date_time=two_weeks_ago)
        response = self.get_response(user=office_hour.mentor,
                                     date_spec=date_spec)
        self.assert_hour_in_response(response, office_hour)

    def test_date_specified_does_not_see_sessions_not_in_range(self):
        two_weeks_ago = days_from_now(-14)
        date_spec = two_weeks_ago.strftime(ISO_8601_DATE_FORMAT)
        office_hour = self.create_office_hour()
        response = self.get_response(user=office_hour.mentor,
                                     date_spec=date_spec)
        self.assert_hour_not_in_response(response, office_hour)

    def test_hours_returned_in_date_sorted_order(self):
        one_day = timedelta(1)
        wednesday = utc.localize(datetime(2020, 1, 31))
        date_spec = wednesday.strftime(ISO_8601_DATE_FORMAT)
        office_hour = self.create_office_hour(start_date_time=wednesday)
        self.create_office_hour(start_date_time=wednesday-one_day,
                                mentor=office_hour.mentor)
        self.create_office_hour(start_date_time=wednesday+one_day,
                                mentor=office_hour.mentor)
        response = self.get_response(user=office_hour.mentor,
                                     date_spec=date_spec)
        self.assert_sessions_sorted_by_date(response)

    def test_user_with_no_hours_sees_empty_response(self):
        user = self.basic_user()
        self.create_office_hour()
        response = self.get_response(user=user)
        sessions = response.data['calendar_data']
        self.assertEqual(len(sessions), 0)

    def test_user_with_no_hours_gets_success_response(self):
        user = self.basic_user()
        self.create_office_hour()
        response = self.get_response(user=user)
        self.assert_success(response)

    def test_user_with_no_hours_in_range_sees_empty_response(self):
        two_weeks_ago = days_from_now(-14)
        session = self.create_office_hour(start_date_time=two_weeks_ago)
        response = self.get_response(user=session.mentor)
        sessions = response.data['calendar_data']
        self.assertEqual(len(sessions), 0)

    def test_user_with_no_hours_in_range_sees_success_response(self):
        two_weeks_ago = days_from_now(-14)
        session = self.create_office_hour(start_date_time=two_weeks_ago)
        response = self.get_response(user=session.mentor)
        self.assert_success(response)

    def test_return_includes_session_timezones(self):
        office_hour = self.create_office_hour()
        timezones = ["America/New_York", "Asia/Jerusalem", "Africa/Accra"]
        for tz in timezones:
            self.create_office_hour(timezone=tz,
                                    mentor=office_hour.mentor)
        response = self.get_response(target_user_id=office_hour.mentor_id)
        response_timezones = set(response.data['timezones'])
        self.assertSetEqual(response_timezones, set(timezones))

    def test_return_includes_mentor_locations(self):
        office_hour = self.create_office_hour()
        user_role = get_user_role_by_name(UserRole.MENTOR)
        locations = LocationFactory.create_batch(3)
        program_families = ProgramFamilyFactory.create_batch(3)
        [ProgramFamilyLocationFactory(location=location,
                                      program_family=program_family)
         for (location, program_family) in zip(locations, program_families)]

        [ProgramRoleGrantFactory(
            person=office_hour.mentor,
            program_role__user_role=user_role,
            program_role__program__program_status="active",
            program_role__program__program_family=program_family)
         for program_family in program_families]

        response = self.get_response(user=office_hour.mentor)
        response_locations = response.data['location_choices']
        self.assertTrue(all([(loc.name, loc.id) in response_locations
                             for loc in locations]))

    def test_bad_date_spec_gets_fail_response(self):
        bad_date_spec = "2020-20-20"  # this cannot be parsed as a date
        response = self.get_response(date_spec=bad_date_spec)
        self.assert_failure(response, self.view.BAD_DATE_SPEC)

    def test_nonexistent_user_gets_fail_response(self):
        bad_user_id = _nonexistent_user_id()
        response = self.get_response(target_user_id=bad_user_id)
        self.assert_failure(response, self.view.NO_SUCH_USER)

    def test_mentor_program_families_in_result(self):
        office_hour = self.create_office_hour()
        user_role = get_user_role_by_name(UserRole.MENTOR)
        prgs = ProgramRoleGrantFactory.create_batch(
            3,
            person=office_hour.mentor,
            program_role__user_role=user_role)
        response = self.get_response(user=office_hour.mentor)
        response_program_families = response.data['mentor_program_families']
        self.assertTrue(all([prg.program_role.program.program_family.name
                             in response_program_families
                             for prg in prgs]))

    def test_no_n_plus_one_queries(self):
        office_hour = self.create_office_hour()
        with CaptureQueriesContext(connection) as captured_queries:
            self.get_response(target_user_id=office_hour.mentor_id)
            total_queries = len(captured_queries)
        [self.create_office_hour(mentor=office_hour.mentor) for _ in range(10)]
        with self.assertNumQueries(total_queries):
            self.get_response(target_user_id=office_hour.mentor_id)

    def test_meeting_info_returned_in_response(self):
        office_hour = self.create_office_hour()
        response = self.get_response(target_user_id=office_hour.mentor_id)
        calendar_data = response.data['calendar_data'][0]
        self.assertIn("meeting_info", calendar_data)

    def create_office_hour(self,
                           mentor=None,
                           finalist=None,
                           start_date_time=None,
                           duration_minutes=30,
                           timezone="America/New_York"):
        create_params = {}
        if mentor:
            create_params['mentor'] = mentor
        duration = timedelta(duration_minutes)
        start_date_time = start_date_time or utc.localize(datetime.now())
        end_date_time = start_date_time + duration
        create_params['start_date_time'] = start_date_time
        create_params['end_date_time'] = end_date_time
        create_params['location__timezone'] = timezone
        return MentorProgramOfficeHourFactory(**create_params)

    def assert_hour_in_response(self, response, hour):
        self.assertTrue(check_hour_in_response(response, hour),
                        msg="The office hour session was not in the response")

    def assert_hour_not_in_response(self, response, hour):
        self.assertFalse(check_hour_in_response(response, hour),
                         msg="The office hour session was in the response")

    def assert_sessions_sorted_by_date(self, response):
        dates = [session['start_date_time']
                 for session in response.data['calendar_data']]
        self.assertEqual(dates, sorted(dates))

    def assert_success(self, response):
        self.assertTrue(response.data['success'])

    def assert_failure(self, response, failure_message):
        data = response.data
        self.assertFalse(data['success'])
        self.assertEqual(data['header'], self.view.FAILURE_HEADER)
        self.assertEqual(data['detail'], failure_message)

    def get_response(self,
                     user=None,
                     target_user_id=None,
                     date_spec=None):
        user = user or self.staff_user()
        user.set_password("password")
        user.save()
        url = reverse(self.view.view_name)
        data = {}
        if date_spec is not None:
            data['date_spec'] = date_spec
        if target_user_id is not None:
            data['user_id'] = target_user_id
        with self.login(email=user.email):
            return self.get(url, data=data)


def check_hour_in_response(response, hour):
    response_data = response.data['calendar_data']
    return hour.id in [response_hour['id']
                       for response_hour in response_data]


def _nonexistent_user_id():
    user = UserFactory()
    user_id = user.id
    user.delete()
    return user_id