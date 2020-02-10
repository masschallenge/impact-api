# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from pytz import utc

from django.urls import reverse

from accelerator.models import UserRole
from accelerator.tests.factories import (
    EntrepreneurFactory,
    ExpertFactory,
    ProgramFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
)

from impact.tests.factories import MentorProgramOfficeHourFactory
from impact.tests.api_test_case import APITestCase
from impact.v1.helpers.mentor_program_office_hour_helper import (
    OFFFICE_HOUR_FIELDS,
)
from impact.tests.utils import assert_fields
from impact.v1.views import MentorProgramOfficeHourListView

USER_OFFICE_HOUR_COUNT = 3
NON_USER_OFFICE_HOUR_COUNT = 4
NON_EXISTENT_ID = 999
NON_EXISTENT_NAME = 'qwerty'


class TestMentorProgramOfficeHourListView(APITestCase):
    url = reverse(MentorProgramOfficeHourListView.view_name)

    def setUp(self):
        self.test_office_hours = MentorProgramOfficeHourFactory.create_batch(
            NON_USER_OFFICE_HOUR_COUNT
        )

    def tearDown(self):
        map(lambda obj: obj.delete(), self.test_office_hours)

    def test_get(self):
        _, office_hours = self._create_user_office_hours()
        response = self._get_response_as_logged_in_user()
        total_count = USER_OFFICE_HOUR_COUNT + NON_USER_OFFICE_HOUR_COUNT
        self.assertEqual(response.data["count"], total_count)
        self.assertTrue(self._compare_ids(office_hours, response))
        self.assertTrue(self._compare_ids(self.test_office_hours, response))

    def test_get_options_match_model_helper_fields(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            self.assertEqual(response.status_code, 200)
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(OFFFICE_HOUR_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):
            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)
            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            self.assertTrue(
                validator.is_valid(json.loads(get_response.content)))

    def test_filters_by_mentor_id(self):
        mentor, mentor_office_hours = self._create_user_office_hours()
        self._check_response_values(
            {'mentor_id': mentor.id},
            mentor_office_hours
        )

    def test_filters_by_mentor_name(self):
        mentor, mentor_office_hours = self._create_user_office_hours()
        self._check_response_values(
            {'mentor_name': mentor.full_name()},
            mentor_office_hours
        )

    def test_nonexistent_mentor_id_returns_nothing(self):
        mentor, mentor_office_hours = self._create_user_office_hours()
        self._assert_nil_response_values(
            {'mentor_id': NON_EXISTENT_ID}
        )

    def test_nonexistent_mentor_name_returns_nothing(self):
        mentor, mentor_office_hours = self._create_user_office_hours()
        self._assert_nil_response_values(
            {'mentor_name': NON_EXISTENT_NAME}
        )

    def test_filters_by_finalist_id(self):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        self._check_response_values(
            {'finalist_id': finalist.id},
            finalist_office_hours
        )

    def test_filters_by_finalist_name(self):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        self._check_response_values(
            {'finalist_name': finalist.full_name()},
            finalist_office_hours
        )

    def test_filters_by_partial_finalist_name(self):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        self._check_response_values(
            {'finalist_name': finalist.first_name},
            finalist_office_hours
        )

    def test_filters_by_user_name(self):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        mentor_with_same_name = ExpertFactory(first_name=finalist.first_name)
        MentorProgramOfficeHourFactory(mentor=mentor_with_same_name)
        response = self._get_response_as_logged_in_user(
            {'user_name': finalist.first_name},
        )
        self.assertEqual(response.data["count"], USER_OFFICE_HOUR_COUNT+1)

    def test_nonexistent_finalist_id_returns_nothing(self):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        self._assert_nil_response_values(
            {'finalist_id': NON_EXISTENT_ID}
        )

    def test_nonexistent_finalist_name_returns_nothing(self):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        self._assert_nil_response_values(
            {'finalist_name': NON_EXISTENT_NAME}
        )

    def test_filters_by_both_mentor_id_and_finalist_id(self):
        self._assert_response_for_params_of_type('id')

    def test_filters_by_both_mentor_name_and_finalist_name(self):
        self._assert_response_for_params_of_type('name')

    def test_only_upcoming_office_hours_are_returned(self):
        yesterday_offset = -2
        tomorrow_offset = 1
        mentor = ExpertFactory()
        MentorProgramOfficeHourFactory(
            mentor=mentor,
            start_date_time=self._get_office_hour_date(yesterday_offset, 10),
            end_date_time=self._get_office_hour_date(yesterday_offset, 12))
        tomorrow_office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor,
            start_date_time=self._get_office_hour_date(tomorrow_offset, 10),
            end_date_time=self._get_office_hour_date(tomorrow_offset, 12))
        response = self._get_response_as_logged_in_user({
            'mentor_id': mentor.id,
            'upcoming': ""})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]['id'],
                         tomorrow_office_hour.pk)

    def test_only_the_user_open_upcoming_hours_are_returned(self):
        tomorrow_offset = 1
        mentor = ExpertFactory()
        program = ProgramFactory()
        user = self.basic_user()
        user_role = UserRole.FINALIST
        pr = ProgramRoleFactory(program=program,
                                user_role__name=user_role)
        ProgramRoleGrantFactory(person=user, program_role=pr,
                                program_role__user_role__name=user_role)
        self.mentor = mentor
        self._create_office_hours(tomorrow_offset, 13, program, user)
        user_open_upcoming_hour = self._create_office_hours(
            tomorrow_offset, 15, program)
        params = {
            'mentor_id': mentor.id,
            'upcoming': "",
            'my_hours': "",
        }
        response = self._get_response_as_logged_in_user(params, user)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]['id'],
                         user_open_upcoming_hour.pk)

    def _create_office_hours(self, offset, hour, program, finalist=None):
        hour = MentorProgramOfficeHourFactory(
            mentor=self.mentor,
            program=program,
            finalist=finalist,
            start_date_time=self._get_office_hour_date(offset, hour),
            end_date_time=self._get_office_hour_date(offset, hour+1)
        )
        return hour

    def _get_office_hour_date(self, day_offset, hour):
        return utc.localize(
            datetime.combine(date.today() + timedelta(days=day_offset),
                             time(hour=hour)))

    def _assert_response_for_params_of_type(
            self, param_type):
        finalist, finalist_office_hours = self._create_user_office_hours(
            mentor=False
        )
        mentor, mentor_office_hours = self._create_user_office_hours()
        mentor_finalist_office_hour = MentorProgramOfficeHourFactory(
            finalist=finalist, mentor=mentor)
        params = self._generate_params(finalist, mentor, param_type)
        response = self._get_response_as_logged_in_user(params)
        self.assertEqual(response.data["count"], 1)
        self.assertTrue(
            response.data["results"][0]["id"], mentor_finalist_office_hour.id)

    def _generate_params(self, finalist, mentor, param_type='id'):
        if param_type == 'id':
            return {
                'finalist_id': finalist.id,
                'mentor_id': mentor.id
            }
        return {
            'finalist_name': finalist.first_name,
            'mentor_name': mentor.last_name
        }

    def _check_response_values(self, params, office_hours):
        response = self._get_response_as_logged_in_user(params)
        self.assertEqual(response.data["count"], USER_OFFICE_HOUR_COUNT)
        self.assertTrue(self._compare_ids(office_hours, response))

    def _assert_nil_response_values(self, params):
        response = self._get_response_as_logged_in_user(params)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def _create_user_office_hours(self, mentor=True):
        if mentor:
            user = ExpertFactory()
            office_hours = MentorProgramOfficeHourFactory.create_batch(
                USER_OFFICE_HOUR_COUNT, mentor=user)
        else:
            user = EntrepreneurFactory()
            office_hours = MentorProgramOfficeHourFactory.create_batch(
                USER_OFFICE_HOUR_COUNT, finalist=user)
        return user, office_hours

    def _get_response_as_logged_in_user(self, params=None, user=None):
        if user:
            self.login(email=user.email)
        else:
            self.login(email=self.basic_user().email)
        return self.client.get(self.url, params)

    def _compare_ids(self, office_hours, response):
        result_ids = [
            result['id'] for result in response.data["results"]
        ]
        return all(
            [office_hour.id in result_ids for office_hour in office_hours])
