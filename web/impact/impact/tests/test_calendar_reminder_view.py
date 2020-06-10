# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from pytz import timezone
from add2cal import Add2Cal
from .api_test_case import APITestCase

from .factories import UserFactory

User = get_user_model()  # pylint: disable=invalid-name

VCALENDAR_HEADER_TEXT = 'BEGIN:VCALENDAR'
CALENDAR_MEDIA_TYPE = 'application/octet-stream'


class TestCalendarReminderView(APITestCase):
    client_class = APIClient
    user_factory = UserFactory

    def setUp(self):
        self.test_params = {
            "start": "20190523T144641",
            "end": "20190523T144641",
            "title": "mentoring session with dj shank",
            'location': 'boston',
            'description': 'test',
            'timezone': timezone('America/New_York')
        }
        self.add2cal = Add2Cal(
            start=self.test_params['start'],
            end=self.test_params['end'],
            title=self.test_params['title'],
            location=self.test_params['location'],
            description=self.test_params['description'],
            timezone=self.test_params['timezone'],
        )

    def test_outlook_reminder_link(self):
        self.maxDiff = None
        with self.login(email=self.basic_user().email):
            self.test_params.update({"link_type": "outlook"})
            response = self.get("calendar_reminder_view",
                                data=self.test_params)
            self.response_302()
        self.assertEqual(
            response.url.split("uid")[0],
            self.add2cal.as_dict()['outlook_link'].split("uid")[0]
        )

    def test_gcal_reminder_link(self):
        with self.login(email=self.basic_user().email):
            self.test_params.update({"link_type": "google"})
            response = self.get("calendar_reminder_view",
                                data=self.test_params)
            self.response_302()
        self.assertEqual(
            response.url.split("uid")[0],
            self.add2cal.as_dict()['gcal_link'].split("uid")[0]
        )

    def test_yahoo_reminder_link(self):
        with self.login(email=self.basic_user().email):
            self.test_params.update({"link_type": "yahoo"})
            response = self.get("calendar_reminder_view",
                                data=self.test_params)
            self.response_302()
        self.assertEqual(
            response.url.split("uid")[0],
            self.add2cal.as_dict()['yahoo_link'].split("uid")[0]
        )

    def test_ical_reminder_link(self):
        with self.login(email=self.basic_user().email):
            self.test_params.update({"link_type": "ical"})
            response = self.get("calendar_reminder_view",
                                data=self.test_params)
            self.response_200()
        self.assertEqual(
            response.request['CONTENT_TYPE'], CALENDAR_MEDIA_TYPE)
        self.assertTrue(
            response.content.decode().startswith(VCALENDAR_HEADER_TEXT))
