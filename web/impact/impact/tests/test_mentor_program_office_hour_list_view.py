# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

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


class TestMentorProgramOfficeHourListView(APITestCase):
    url = reverse(MentorProgramOfficeHourListView.view_name)

    def test_get(self):
        count = 5
        office_hours = MentorProgramOfficeHourFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            self.assertEqual(response.data["count"], count)
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
        mentor_count = 2
        mentor, mentor_office_hours = self._create_office_hours_for_user(
            mentor_count)
        response = self._get_response_as_logged_in_user(
            {'mentor_id': mentor.id}
        )
        self.assertEqual(response.data["count"], mentor_count)
        self.assertTrue(self._compare_ids(mentor_office_hours, response))

    def test_filters_by_finalist_id(self):
        finalist_count = 1
        finalist, finalist_office_hours = self._create_office_hours_for_user(
            finalist_count, mentor=False
        )
        response = self._get_response_as_logged_in_user(
            {'finalist_id': finalist.id}
        )
        self.assertEqual(response.data["count"], finalist_count)
        self.assertTrue(self._compare_ids(finalist_office_hours, response))

    def _create_office_hours_for_user(self, count=1, mentor=True):
        if mentor:
            user = ExpertFactory()
            office_hours = MentorProgramOfficeHourFactory.create_batch(
                count, mentor=user)
        else:
            user = EntrepreneurFactory()
            office_hours = MentorProgramOfficeHourFactory.create_batch(
                count, finalist=user)

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
