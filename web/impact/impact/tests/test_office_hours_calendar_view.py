from datetime import (
    datetime,
    timedelta,
)
from pytz import utc

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from .api_test_case import APITestCase
from ..v1.views import (
    ISO_8601_DATE_FORMAT,
    OfficeHoursCalendarView,
)
from ..v1.views.office_hours_calendar_view import FINALIST, MENTOR, STAFF
from ..permissions.v1_api_permissions import DEFAULT_PERMISSION_DENIED_DETAIL
from .factories import UserFactory
from .utils import nonexistent_object_id
from accelerator.tests.factories import (
    LocationFactory,
    MentorProgramOfficeHourFactory,
    ProgramFactory,
    ProgramFamilyFactory,
    ProgramFamilyLocationFactory,
    ProgramRoleGrantFactory,
    StartupTeamMemberFactory,
)
from accelerator.tests.contexts import UserRoleContext
from accelerator.tests.contexts.context_utils import get_user_role_by_name
from accelerator.tests.utils import days_from_now
from accelerator_abstract.models.base_clearance import (
                                                        CLEARANCE_LEVEL_EXEC_MD,
                                                        CLEARANCE_LEVEL_GLOBAL_MANAGER,
                                                        CLEARANCE_LEVEL_POM,
                                                        CLEARANCE_LEVEL_STAFF
                                                        )
from mc.utils import swapper_model

UserRole = swapper_model("UserRole")


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
        user = _mentor()
        self.create_office_hour()
        response = self.get_response(user=user)
        sessions = response.data['calendar_data']
        self.assertEqual(len(sessions), 0)

    def test_user_with_no_hours_gets_success_response(self):
        user = _mentor()
        self.create_office_hour()
        response = self.get_response(user=user)
        self.assert_success(response)

    def test_current_finalist_sees_current_reserved_hours(self):
        finalist = _finalist()
        office_hour = self.create_office_hour(finalist=finalist)
        response = self.get_response(user=finalist)
        self.assert_hour_in_response(response, office_hour)

    def test_current_finalist_sees_current_open_hours(self):
        program = ProgramFactory()
        finalist = _finalist(program=program)
        mentor = _mentor(program=program)
        office_hour = self.create_office_hour(mentor=mentor)
        response = self.get_response(user=finalist)
        self.assert_hour_in_response(response, office_hour)

    def test_current_finalist_sees_only_relevant_open_hours(self):
        program = ProgramFactory()
        finalist = _finalist(program=program)
        office_hour = self.create_office_hour()
        response = self.get_response(user=finalist)
        self.assert_hour_not_in_response(response, office_hour)

    def test_staff_sees_current_open_hours_for_their_program(self):
        program = ProgramFactory()
        staff_user = self.staff_user(program_family=program.program_family)
        mentor = _mentor(program=program)
        office_hour = self.create_office_hour(mentor=mentor)
        response = self.get_response(user=staff_user)
        self.assert_hour_in_response(response, office_hour)

    def test_staff_sees_own_office_hour_flag_for_their_hours(self):
        program = ProgramFactory()
        staff_user = self.staff_user(program_family=program.program_family)
        _mentor(program=program, user=staff_user)
        self.create_office_hour(mentor=staff_user)
        response = self.get_response(user=staff_user)
        office_hour_data = response.data['calendar_data'][0]
        self.assertTrue(office_hour_data['own_office_hour'])

    def test_staff_sees_only_relevant_open_hours(self):
        program = ProgramFactory()
        staff_user = self.staff_user(program_family=program.program_family)
        office_hour = self.create_office_hour()
        response = self.get_response(staff_user)
        self.assert_hour_not_in_response(response, office_hour)

    def test_non_staff_cannot_view_on_behalf_of(self):
        user = self.basic_user()
        finalist = _finalist()
        response = self.get_response(user=user,
                                     target_user_id=finalist.id)
        self.assert_failure(response,
                            DEFAULT_PERMISSION_DENIED_DETAIL)

    def test_mentor_with_no_hours_in_range_sees_empty_response(self):
        two_weeks_ago = days_from_now(-14)
        session = self.create_office_hour(start_date_time=two_weeks_ago)
        response = self.get_response(user=session.mentor)
        sessions = response.data['calendar_data']
        self.assertEqual(len(sessions), 0)

    def test_mentor_with_no_hours_in_range_sees_success_response(self):
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
        response = self.get_response(user=office_hour.mentor)
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
        response_location_names = [
            location['location_name'] for location in response_locations]
        self.assertTrue(all([loc.name in response_location_names
                             for loc in locations]))

    def test_response_data_includes_user_startups(self):
        self.create_office_hour()
        finalist = _finalist()
        stms = StartupTeamMemberFactory.create_batch(5, user=finalist)
        startup_names = [stm.startup.name for stm in stms]
        response = self.get_response(user=finalist)
        response_startup_names = response.data['user_startups'].values_list(
            "name",
            flat=True)
        self.assertTrue(all([name in response_startup_names
                             for name in startup_names]))

    def test_bad_date_spec_gets_fail_response(self):
        bad_date_spec = "2020-20-20"  # this cannot be parsed as a date
        response = self.get_response(date_spec=bad_date_spec)
        self.assert_failure(response, self.view.BAD_DATE_SPEC)

    def test_nonexistent_user_gets_fail_response(self):
        bad_user_id = nonexistent_object_id(UserFactory)
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

    def test_non_office_hour_viewer_user_sees_no_hours(self):
        user = _judge()  # judges are not office hour viewers
        office_hour = self.create_office_hour()
        response = self.get_response(user=user)
        self.assert_hour_not_in_response(response, office_hour)

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

    def test_user_with_staff_clearance_sees_own_office_hour(self):
        self.assert_user_with_clearance_sees_own_office_hour(
            CLEARANCE_LEVEL_STAFF)

    def test_location_choices_for_staff_with_clearance_in_response(self):
        program_family_location = ProgramFamilyLocationFactory()
        program_family = program_family_location.program_family
        location = program_family_location.location
        ProgramFactory(program_family=program_family)
        staff_user = self.staff_user(program_family=program_family)
        self.create_office_hour(mentor=staff_user)
        response = self.get_response(user=staff_user)
        location_choices = response.data['location_choices']
        response_location_names = [
            location['location_name'] for location in location_choices]
        self.assertTrue(location.name in response_location_names)

    def test_program_family_for_staff_with_clearance_in_response(self):
        program_family = ProgramFactory().program_family
        staff_user = self.staff_user(program_family=program_family)
        self.create_office_hour(mentor=staff_user)
        response = self.get_response(user=staff_user)
        mentor_program_families = response.data['mentor_program_families']
        self.assertTrue(program_family.name in mentor_program_families)

    def test_mentor_user_type_is_returned_in_response(self):
        response = self.get_response(user=_mentor())
        self.assert_correct_user_type(response, MENTOR)

    def test_finalist_user_type_is_returned_in_response(self):
        response = self.get_response(user=_finalist())
        self.assert_correct_user_type(response, FINALIST)

    def test_staff_user_type_is_returned_in_response(self):
        response = self.get_response()
        self.assert_correct_user_type(response, STAFF)

    def test_timezone_response_data_excludes_null_values(self):
        office_hour = self.create_office_hour(timezone=None)
        response = self.get_response(target_user_id=office_hour.mentor_id)
        timezone_data = response.data['timezones']
        self.assertEqual(timezone_data.count(), 0)

    def test_location_always_include_remote_location(self):
        program_family_location = ProgramFamilyLocationFactory()
        program_family = program_family_location.program_family
        remote_location = LocationFactory(name="Remote")
        ProgramFactory(program_family=program_family)
        staff_user = self.staff_user(program_family=program_family)
        self.create_office_hour(mentor=staff_user)
        response = self.get_response(user=staff_user)
        location_choices = response.data['location_choices']
        response_location_names = [
            location['location_name'] for location in location_choices]
        self.assertTrue(remote_location.name in response_location_names)

    def test_user_with_pom_clearance_sees_own_office_hour(self):
        self.assert_user_with_clearance_sees_own_office_hour(
            CLEARANCE_LEVEL_POM)

    def test_user_with_exec_md_clearance_sees_own_office_hour(self):
        self.assert_user_with_clearance_sees_own_office_hour(
            CLEARANCE_LEVEL_EXEC_MD)

    def test_global_manager_sees_own_office_hour(self):
        self.assert_user_with_clearance_sees_own_office_hour(
            CLEARANCE_LEVEL_GLOBAL_MANAGER)

    def create_office_hour(self,
                           mentor=None,
                           finalist=None,
                           start_date_time=None,
                           duration_minutes=30,
                           timezone="America/New_York",
                           program=None,
                           location=None):
        create_params = {}
        mentor = mentor or _mentor(program)
        create_params['mentor'] = mentor
        duration = timedelta(duration_minutes)
        start_date_time = start_date_time or utc.localize(datetime.now())
        end_date_time = start_date_time + duration
        create_params['start_date_time'] = start_date_time
        create_params['end_date_time'] = end_date_time
        create_params['location__timezone'] = timezone
        create_params['finalist'] = finalist
        create_params['program'] = program
        if not timezone:
            create_params['location'] = location
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
        self.assertEqual(data['header'], self.view.FAIL_HEADER)
        self.assertEqual(data['detail'], failure_message)

    def assert_correct_user_type(self, response, user_type):
        self.assertEqual(response.data['user_type'], user_type)

    def assert_user_with_clearance_sees_own_office_hour(self, clearance_level):
        program = ProgramFactory()
        staff_user = self.staff_user(program_family=program.program_family,
                                     level=clearance_level)
        office_hour = self.create_office_hour(mentor=staff_user)
        response = self.get_response(user=staff_user)
        self.assert_hour_in_response(response, office_hour)

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


def _user_with_role(role_name, program, user):
    program = program or ProgramFactory()
    return UserRoleContext(role_name, program=program, user=user).user


def _finalist(program=None, user=None):
    return _user_with_role(UserRole.FINALIST, program, user)


def _mentor(program=None, user=None):
    return _user_with_role(UserRole.MENTOR, program, user)


def _judge(program=None, user=None):
    return _user_with_role(UserRole.JUDGE, program, user)
