# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from django.contrib.auth import get_user_model
from impact.models import (
    EntrepreneurProfile,
    ExpertProfile,
    MemberProfile
)
import pytz
from impact.tests.factories import StartupTeamMemberFactory
from impact.tests.contexts import UserContext
from impact.tests.api_test_case import APITestCase
import simplejson as json
from impact.v1.views.user_list_view import EMAIL_EXISTS_ERROR
import datetime

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

    def test_updated_at_lt_datetime_filter(self):
        user = UserContext().user
        user2 = UserContext().user
        user3 = UserContext().user
        StartupTeamMemberFactory(user=user)
        StartupTeamMemberFactory(user=user2)
        StartupTeamMemberFactory(user=user3)
        response = ""
        lastweek = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        EntrepreneurProfile.objects.filter(user__id=user.id).update(
            updated_at=lastweek)
        with self.login(username=self.basic_user().username):
            url = "{base_url}?updated_at__lt={datestr}".format(
                base_url=reverse("user"),
                datestr=lastweek.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['count'], 0)

    def test_updated_at_gt_datetime_filter(self):
        user = UserContext().user
        user2 = UserContext().user
        user3 = UserContext().user
        StartupTeamMemberFactory(user=user)
        StartupTeamMemberFactory(user=user2)
        StartupTeamMemberFactory(user=user3)
        response = ""
        lastweek = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        EntrepreneurProfile.objects.all().update(
            updated_at=datetime.datetime.now(pytz.utc))
        ExpertProfile.objects.all().update(
            updated_at=datetime.datetime.now(pytz.utc))
        MemberProfile.objects.all().update(
            updated_at=datetime.datetime.now(pytz.utc))
        EntrepreneurProfile.objects.filter(user__id=user.id).update(
            updated_at=lastweek)
        with self.login(username=self.basic_user().username):
            url = "{base_url}?updated_at__gt={datestr}".format(
                base_url=reverse("user"),
                datestr=lastweek.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
        response_json = json.loads(response.content)
        contains_user = False
        for result in response_json['results']:
            if result['id'] == user.id:
                contains_user = True
                break
        self.assertTrue(contains_user)
