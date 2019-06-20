# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from accelerator.tests.factories import (
    EntrepreneurFactory,
    ExpertFactory,
)

from impact.tests.factories import MentorProgramOfficeHourFactory
from impact.tests.api_test_case import APITestCase
from impact.v1.helpers.mentor_program_office_hour_helper import (
    OFFFICE_HOUR_FIELDS,
)
from impact.tests.utils import assert_fields
from impact.v1.views import MentorProgramOfficeHourListView

COUNT = 3
NON_EXISTENT_ID = 999
NON_EXISTENT_NAME = 'qwerty'


class TestMentorProgramOfficeHourListView(APITestCase):
    url = reverse(MentorProgramOfficeHourListView.view_name)

    def test_get(self):
        office_hours = MentorProgramOfficeHourFactory.create_batch(COUNT)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            self.assertEqual(response.data["count"], COUNT)
            self.assertTrue(self._compare_ids(office_hours, response))

    def test_options(self):
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
        mentor, mentor_office_hours = self._create_office_hours()
        self._check_response_values(
            {'mentor_id': mentor.id},
            mentor_office_hours
        )

    def test_filters_by_mentor_name(self):
        mentor, mentor_office_hours = self._create_office_hours()
        self._check_response_values(
            {'mentor_name': mentor.full_name()},
            mentor_office_hours
        )

    def test_nonexistent_mentor_id_returns_nothing(self):
        mentor, mentor_office_hours = self._create_office_hours()
        self._assert_nil_response_values(
            {'mentor_id': NON_EXISTENT_ID}
        )

    def test_nonexistent_mentor_name_returns_nothing(self):
        mentor, mentor_office_hours = self._create_office_hours()
        self._assert_nil_response_values(
            {'mentor_name': NON_EXISTENT_NAME}
        )

    def test_filters_by_finalist_id(self):
        finalist, finalist_office_hours = self._create_office_hours(
            mentor=False
        )
        self._check_response_values(
            {'finalist_id': finalist.id},
            finalist_office_hours
        )

    def test_filters_by_finalist_name(self):
        finalist, finalist_office_hours = self._create_office_hours(
            mentor=False
        )
        self._check_response_values(
            {'finalist_name': finalist.full_name()},
            finalist_office_hours
        )

    def test_filters_by_partial_finalist_name(self):
        finalist, finalist_office_hours = self._create_office_hours(
            mentor=False
        )
        self._check_response_values(
            {'finalist_name': finalist.first_name},
            finalist_office_hours
        )

    def test_nonexistent_finalist_id_returns_nothing(self):
        finalist, finalist_office_hours = self._create_office_hours(
            mentor=False
        )
        self._assert_nil_response_values(
            {'finalist_id': NON_EXISTENT_ID}
        )

    def test_nonexistent_finalist_name_returns_nothing(self):
        finalist, finalist_office_hours = self._create_office_hours(
            mentor=False
        )
        self._assert_nil_response_values(
            {'finalist_name': NON_EXISTENT_NAME}
        )

    def _check_response_values(self, params, office_hours):
        response = self._get_response_as_logged_in_user(params)
        self.assertEqual(response.data["count"], COUNT)
        self.assertTrue(self._compare_ids(office_hours, response))

    def _assert_nil_response_values(self, params):
        response = self._get_response_as_logged_in_user(params)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def _create_office_hours(self, mentor=True):
        if mentor:
            user = ExpertFactory()
            office_hours = MentorProgramOfficeHourFactory.create_batch(
                COUNT, mentor=user)
        else:
            user = EntrepreneurFactory()
            office_hours = MentorProgramOfficeHourFactory.create_batch(
                COUNT, finalist=user)
        # create office hours not associated with user
        MentorProgramOfficeHourFactory.create_batch(4)
        return user, office_hours

    def _get_response_as_logged_in_user(self, params):
        self.login(email=self.basic_user().email)
        return self.client.get(self.url, params)

    def _compare_ids(self, office_hours, response):
        office_hour_ids = [
            office_hour.id for office_hour in office_hours]
        result_ids = [
            result['id'] for result in response.data["results"]
        ]
        return office_hour_ids == result_ids
