# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from add2cal import Add2Cal
from impact.tests.api_test_case import APITestCase

from impact.tests.factories import UserFactory

User = get_user_model()  # pylint: disable=invalid-name


class TestCalendarReminderView(APITestCase):
    client_class = APIClient
    user_factory = UserFactory

    def setUp(self):
        self.add2cal = Add2Cal(
            start=float(1558634110),
            end=float(1558634120),
            title="mentoring session with dj shank",
            location='boston',
            description='test'
        )

    def test_outlook_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "outlook",
                "start": "1558634110",
                "end": "1558634120",
                "title": "mentoring session with dj shank",
                'location': 'boston',
                'description': 'test'
            }
            response = self.get("calendar_reminder_view", data=params)
            self.response_302()
        self.assertEquals(
            response.url,
            self.add2cal.as_dict()['outlook_link']
        )
        self.assertEquals(302, response.status_code)

    def test_gcal_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "google",
                "start": "1558634110",
                "end": "1558634120",
                "title": "mentoring session with dj shank",
                'location': 'boston',
                'description': 'test'
            }
            response = self.get("calendar_reminder_view", data=params)
            self.response_302()
        print(self.add2cal.as_dict()['gcal_link'])
        self.assertEquals(
            response.url,
            self.add2cal.as_dict()['gcal_link']
        )
        self.assertEquals(302, response.status_code)

    def test_yahoo_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "yahoo",
                "start": "1558634110",
                "end": "1558634120",
                "title": "mentoring session with dj shank",
                'location': 'boston',
                'description': 'test'
            }
            response = self.get("calendar_reminder_view", data=params)
            self.response_302()
        self.assertEquals(
            response.url,
            self.add2cal.as_dict()['yahoo_link']
        )
        self.assertEquals(302, response.status_code)

    def test_ical_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "ical",
                "start": "1558634110",
                "end": "1558634120",
                "title": "mentoring session with dj shank",
                'location': 'boston',
                'description': 'test'
            }
            response = self.get("calendar_reminder_view", data=params)
            self.response_200()
        self.assertEquals(response.content_type, 'text/calendar')
        self.assertTrue(response.data.startswith('BEGIN:VCALENDAR'))
