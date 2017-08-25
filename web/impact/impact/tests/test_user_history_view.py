# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    UserFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.tests.utils import find_events
from impact.v1.events import (
    UserCreatedEvent,
)


class TestUserHistoryView(APITestCase):
    def test_user_created(self):
        user = UserFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[user.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 UserCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(user.date_joined, events[0]["datetime"])
