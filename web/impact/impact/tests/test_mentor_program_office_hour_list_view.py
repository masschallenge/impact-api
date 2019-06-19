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
            self.assertTrue(all(
                [MentorProgramOfficeHourListView.serialize(office_hour)
                 in response.data["results"]
                 for office_hour in office_hours]))

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
            assert validator.is_valid(json.loads(get_response.content))

    def test_filters_by_mentor_id(self):
        mentor_1_count = 3
        mentor_1 = ExpertFactory()
        mentor_1_office_hours = MentorProgramOfficeHourFactory.create_batch(
            mentor_1_count, mentor=mentor_1)
        mentor_2_count = 2
        mentor_2 = ExpertFactory()
        MentorProgramOfficeHourFactory.create_batch(
            mentor_2_count, mentor=mentor_2)

        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url, {'mentor_id': mentor_1.id})
            self.assertEqual(
                response.data["count"], mentor_1_count)
            self.assertTrue(all(
                [MentorProgramOfficeHourListView.serialize(office_hour)
                 in response.data["results"]
                 for office_hour in mentor_1_office_hours]))

    def test_filters_by_mentor_email(self):
        mentor_1_count = 3
        mentor_1 = ExpertFactory()
        MentorProgramOfficeHourFactory.create_batch(
            mentor_1_count, mentor=mentor_1)
        mentor_2_count = 2
        mentor_2 = ExpertFactory()
        mentor_2_office_hours = MentorProgramOfficeHourFactory.create_batch(
            mentor_2_count, mentor=mentor_2)

        with self.login(email=self.basic_user().email):
            response = self.client.get(
                self.url, {'mentor_email': mentor_2.email})
            self.assertEqual(
                response.data["count"], mentor_2_count)
            self.assertTrue(all(
                [MentorProgramOfficeHourListView.serialize(office_hour)
                 in response.data["results"]
                 for office_hour in mentor_2_office_hours]))

    def test_filters_by_finalist_id(self):
        finalist = EntrepreneurFactory()
        MentorProgramOfficeHourFactory.create_batch(5)
        finalist_office_hour = MentorProgramOfficeHourFactory(
            finalist=finalist)

        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url, {'finalist_id': finalist.id})
            self.assertEqual(
                response.data["count"], 1)
            self.assertTrue(
                MentorProgramOfficeHourListView.serialize(finalist_office_hour)
                in response.data["results"])

    def test_filters_by_finalist_email(self):
        finalist = EntrepreneurFactory()
        MentorProgramOfficeHourFactory.create_batch(5)
        finalist_office_hour = MentorProgramOfficeHourFactory(
            finalist=finalist)

        with self.login(email=self.basic_user().email):
            response = self.client.get(
                self.url, {'finalist_email': finalist.email})
            self.assertEqual(
                response.data["count"], 1)
            self.assertTrue(
                MentorProgramOfficeHourListView.serialize(finalist_office_hour)
                in response.data["results"])
