# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import pytz
import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model

from impact.tests.factories import StartupTeamMemberFactory
from impact.tests.contexts import UserContext
from impact.tests.api_test_case import APITestCase
from impact.utils import (
    get_profile,
    override_updated_at,
)
from impact.v1.views.user_list_view import EMAIL_EXISTS_ERROR

EXAMPLE_USER = {
    "first_name": "First",
    "last_name": "Last",
    "email": "test@example.com",
    "gender": "o",
}
User = get_user_model()


class TestUserListView(APITestCase):

    def test_get(self):
        user1 = UserContext().user
        user2 = UserContext().user
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            user_count = User.objects.count()
            response = self.client.get(url)
            results = response.data["results"]
            assert user_count == min(len(results), 10)
            emails = [result["email"] for result in response.data["results"]]
            assert user1.email in emails
            assert user2.email in emails
            assert user_count == response.data["count"]

    def test_get_with_limit(self):
        UserContext().user
        UserContext().user
        with self.login(username=self.basic_user().username):
            url = reverse("user") + "?limit=1"
            user_count = User.objects.count()
            response = self.client.get(url)
            results = response.data["results"]
            assert 1 == len(results)
            assert user_count == response.data["count"]

    def test_post(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, EXAMPLE_USER)
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_USER["email"]

    def test_post_without_required_field(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, {})
            assert response.status_code == 403

    def test_post_bad_key(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            bad_key = "bad key"
            response = self.client.post(url, {bad_key: True})
            assert response.status_code == 403
            assert any([bad_key in error for error in response.data])

    def test_post_with_existing_email(self):
        user = UserContext().user
        data = EXAMPLE_USER.copy()
        data["email"] = user.email
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, data)
            assert response.status_code == 403
            assert EMAIL_EXISTS_ERROR.format(user.email) in response.data

    def test_updated_at_before_datetime_filter(self):
        updated_none = _user_for_date(None)
        week_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        one_day = datetime.timedelta(days=1)
        updated_before = _user_for_date(week_ago - one_day)
        updated_exactly = _user_for_date(week_ago)
        updated_after = _user_for_date(week_ago + one_day)
        with self.login(username=self.basic_user().username):
            url = "{base_url}?updated_at.before={datestr}".format(
                base_url=reverse("user"),
                datestr=week_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
            assert _contains_user(updated_none, response.data)
            assert _contains_user(updated_before, response.data)
            assert _contains_user(updated_exactly, response.data)
            assert not _contains_user(updated_after, response.data)

    def test_updated_at_after_datetime_filter(self):
        updated_none = _user_for_date(None)
        week_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        one_day = datetime.timedelta(days=1)
        updated_before = _user_for_date(week_ago - one_day)
        updated_exactly = _user_for_date(week_ago)
        updated_after = _user_for_date(week_ago + one_day)
        with self.login(username=self.basic_user().username):
            url = "{base_url}?updated_at.after={datestr}".format(
                base_url=reverse("user"),
                datestr=week_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
            assert not _contains_user(updated_none, response.data)
            assert not _contains_user(updated_before, response.data)
            assert _contains_user(updated_exactly, response.data)
            assert _contains_user(updated_after, response.data)


def _user_for_date(date):
    user = UserContext().user
    StartupTeamMemberFactory(user=user)
    override_updated_at(get_profile(user), date)
    return user


def _contains_user(user, data):
    for result in data["results"]:
        if result["id"] == user.id:
            return True
    return False
