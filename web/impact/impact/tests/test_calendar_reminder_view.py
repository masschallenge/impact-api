# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from add2cal import Add2Cal
from .tests.api_test_case import APITestCase

from .tests.factories import UserFactory

User = get_user_model()  # pylint: disable=invalid-name

VCALENDAR_HEADER_TEXT = 'BEGIN:VCALENDAR'
CALENDAR_MEDIA_TYPE = 'application/octet-stream'


class TestCalendarReminderView(APITestCase):
    client_class = APIClient
    user_factory = UserFactory

    def setUp(self):
        self.add2cal = Add2Cal(
            start='20190523T144641',
            end='20190523T144641',
            title="mentoring session with dj shank",
            location='boston',
            description='test'
        )

    def test_outlook_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "outlook",
                "start": "20190523T144641",
                "end": "20190523T144641",
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

    def test_gcal_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "google",
                "start": "20190523T144641",
                "end": "20190523T144641",
                "title": "mentoring session with dj shank",
                'location': 'boston',
                'description': 'test'
            }
            response = self.get("calendar_reminder_view", data=params)
            self.response_302()
        self.assertEquals(
            response.url,
            self.add2cal.as_dict()['gcal_link']
        )

    def test_yahoo_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "yahoo",
                "start": "20190523T144641",
                "end": "20190523T144641",
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

    def test_ical_reminder_link(self):
        with self.login(email=self.basic_user().email):
            params = {
                "link_type": "ical",
                "start": "20190523T144641",
                "end": "20190523T144641",
                "title": "mentoring session with dj shank",
                'location': 'boston',
                'description': 'test'
            }
            response = self.get("calendar_reminder_view", data=params)
            self.response_200()
        self.assertEquals(
            response.request['CONTENT_TYPE'], CALENDAR_MEDIA_TYPE)
        self.assertTrue(
            response.content.decode().startswith(VCALENDAR_HEADER_TEXT))
