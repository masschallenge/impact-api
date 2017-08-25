# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.factories import (
    StartupTeamMemberFactory,
    UserFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.tests.utils import (
    days_from_now,
    find_events,
)
from impact.v1.events import (
    UserCreatedEvent,
    UserJoinedStartupEvent,
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

    def test_user_joined_startup(self):
        stm = StartupTeamMemberFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[stm.user.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 UserJoinedStartupEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(stm.created_at, events[0]["datetime"])

    def test_user_joined_startup_no_created_at(self):
        join_date = days_from_now(-10)
        stm = StartupTeamMemberFactory(user__date_joined=join_date)
        stm.created_at = None
        stm.save()
        next_created_at = days_from_now(-1)
        next_stm = StartupTeamMemberFactory()
        next_stm.created_at = next_created_at
        next_stm.save()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[stm.user.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 UserJoinedStartupEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(join_date, events[0]["datetime"])
            self.assertEqual(next_created_at, events[0]["latest_datetime"])
