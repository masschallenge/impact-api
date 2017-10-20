# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import pytz
import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model

from impact.models import (
    EntrepreneurProfile,
    ExpertProfile,
    MemberProfile,
)
from impact.tests.api_test_case import APITestCase
from impact.tests.contexts import UserContext
from impact.tests.factories import (
    ExpertCategoryFactory,
    IndustryFactory,
    ProgramFamilyFactory,
    StartupTeamMemberFactory,
)
from impact.tests.test_user_detail_view import (
    ENTREPRENEUR_GET_FIELDS,
    EXPERT_MUTABLE_FIELDS,
    EXPERT_ONLY_FIELDS,
    MUTABLE_FIELDS,
    NON_MEMBER_MUTABLE_FIELDS,
    WRITE_ONCE_FIELDS,
)
from impact.tests.utils import (
    assert_fields,
    assert_fields_not_required,
    assert_fields_required,
)
from impact.utils import (
    get_profile,
    override_updated_at,
)
from impact.v1.helpers.model_helper import (
    INVALID_CHOICE_ERROR,
    INVALID_URL_ERROR,
    format_choices,
)
from impact.v1.views.user_list_view import (
    EMAIL_EXISTS_ERROR,
    UNSUPPORTED_KEY_ERROR,
)

EXAMPLE_ENTREPRENEUR = {
    "email": "entrepreneur@example.com",
    "is_active": "true",
    "first_name": "Entre",
    "gender": "f",
    "last_name": "Preneur",
    "user_type": EntrepreneurProfile.user_type,
}
EXAMPLE_EXPERT = {
    "company": "Expert, Co.",
    "email": "expert@example.com",
    "is_active": "true",
    "first_name": "Ex",
    "gender": "f",
    "last_name": "Pert",
    "phone": "123-456-7890",
    "title": "Chief Expert",
    "user_type": ExpertProfile.user_type,
    "speaker_interest": "true",
}
EXAMPLE_MEMBER = {
    "email": "member@example.com",
    "is_active": "false",
    "first_name": "Mem",
    "gender": "o",
    "last_name": "Ber",
    "user_type": MemberProfile.user_type,
}
REQUIRED_POST_FIELDS = set([
        "email",
        "first_name",
        "gender",
        "last_name",
        "user_type",
])
ALL_POST_FIELDS = set(EXPERT_MUTABLE_FIELDS +
                      MUTABLE_FIELDS +
                      NON_MEMBER_MUTABLE_FIELDS +
                      WRITE_ONCE_FIELDS)
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

    def test_options(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["item"]["properties"]
            assert_fields(ENTREPRENEUR_GET_FIELDS, get_options)
            assert_fields(EXPERT_ONLY_FIELDS, get_options)
            post_options = response.data["actions"]["POST"]["properties"]
            assert_fields_required(REQUIRED_POST_FIELDS, post_options)
            assert_fields_not_required(ALL_POST_FIELDS - REQUIRED_POST_FIELDS,
                                       post_options)

    def test_post_entrepreneur(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, EXAMPLE_ENTREPRENEUR)
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_ENTREPRENEUR["email"]
            assert EntrepreneurProfile.objects.get(user=user)

    def test_post_entrepreneur_with_expert_keys(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            data = _example_expert()
            data["user_type"] = EntrepreneurProfile.user_type
            response = self.client.post(url, data)
            error_msg = UNSUPPORTED_KEY_ERROR.format(key="company",
                                                     type=data["user_type"])
            assert error_msg in response.data

    def test_post_expert(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, _example_expert())
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_EXPERT["email"]
            assert ExpertProfile.objects.get(user=user)

    def test_post_expert_with_bad_category(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            bad_name = "Bad Category"
            response = self.client.post(
                url, _example_expert(expert_category=bad_name))
            error_msg = INVALID_CHOICE_ERROR.format(field="expert_category",
                                                    value=bad_name,
                                                    choices=format_choices([]))
            assert error_msg in response.data

    def test_post_expert_with_bad_url(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            bad_url = "Bad URL"
            response = self.client.post(
                url, _example_expert(personal_website_url=bad_url))
            error_msg = INVALID_URL_ERROR.format(field="personal_website_url",
                                                 value=bad_url)
            assert error_msg in response.data

    def test_post_member(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            response = self.client.post(url, EXAMPLE_MEMBER)
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_MEMBER["email"]
            assert MemberProfile.objects.get(user=user)

    def test_post_member_with_bio(self):
        with self.login(username=self.basic_user().username):
            url = reverse("user")
            data = {"bio": "I have a bio!"}
            data.update(EXAMPLE_MEMBER)
            response = self.client.post(url, data)
            error_msg = UNSUPPORTED_KEY_ERROR.format(key="bio",
                                                     type=data["user_type"])
            assert error_msg in response.data

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
        data = EXAMPLE_MEMBER.copy()
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


def _example_expert(**kwargs):
    result = EXAMPLE_MEMBER.copy()
    result.update(kwargs)
    if "home_program_family_id" not in result:
        result["home_program_family_id"] = ProgramFamilyFactory().id
    if "primary_industry_id" not in result:
        result["primary_industry_id"] = IndustryFactory().id
    if "expert_category" not in result:
        result["expert_category"] = ExpertCategoryFactory().name
    result.update(EXAMPLE_EXPERT)
    return result
