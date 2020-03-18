# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import datetime
import json
from jsonschema import Draft4Validator
import pytz

from django.urls import reverse
from django.contrib.auth import get_user_model

from accelerator.models import (
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
    EXPERT_GET_FIELDS,
    EXPERT_WRITE_FIELDS,
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

from impact.v1.helpers.validators import (
    format_choices,
    INVALID_CHOICE_ERROR,
    INVALID_URL_ERROR,
)

from impact.v1.views.base_list_view import (
    DEFAULT_MAX_LIMIT,
    GREATER_THAN_MAX_LIMIT_ERROR,
    KWARG_VALUE_NOT_INTEGER_ERROR,
    KWARG_VALUE_IS_NON_POSITIVE_ERROR,
    KWARG_VALUE_IS_NEGATIVE_ERROR,
)
from impact.v1.views.user_list_view import (
    EMAIL_EXISTS_ERROR,
    UNSUPPORTED_KEY_ERROR,
    UserListView,
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
ALL_POST_FIELDS = set(EXPERT_WRITE_FIELDS +
                      MUTABLE_FIELDS +
                      NON_MEMBER_MUTABLE_FIELDS +
                      WRITE_ONCE_FIELDS)
User = get_user_model()


class TestUserListView(APITestCase):
    url = reverse(UserListView.view_name)

    def test_get(self):
        user1 = UserContext().user
        user2 = UserContext().user
        with self.login(email=self.basic_user().email):
            user_count = User.objects.count()
            response = self.client.get(self.url)
            results = response.data["results"]
            assert user_count == min(len(results), 10)
            emails = [result["email"] for result in response.data["results"]]
            assert user1.email in emails
            assert user2.email in emails
            assert user_count == response.data["count"]

    def test_get_returns_correct_count_attribute(self):
        for _ in range(10):
            UserContext()
        with self.login(email=self.basic_user().email):
            user_count = User.objects.count()
            response = self.client.get(self.url)
            assert user_count == response.data["count"]

    def test_get_with_limit_returns_correct_number_of_results(self):
        limit = 1
        for _ in range(limit * 3):
            UserContext()
        with self.login(email=self.basic_user().email):
            url = self.url + "?limit={}".format(limit)
            response = self.client.get(url)
            results = response.data["results"]
            assert limit == len(results)

    def test_get_correct_pagination_attributes_for_offset_zero(self):
        limit = 3
        current_implicit_offset = 0
        for _ in range(limit * 3):
            UserContext()
        with self.login(email=self.basic_user().email):
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            results = response.data["results"]
            assert limit == len(results)
            assert response.data["previous"] is None
            assert limit_arg in response.data["next"]
            next_offset_arg = "offset={}".format(
                current_implicit_offset + limit)
            assert next_offset_arg in response.data["next"]

    def test_get_pagination_attrs_for_offset_between_zero_and_limit(self):
        limit = 4
        current_offset = limit - 2
        for _ in range(limit * 3):
            UserContext()
        with self.login(email=self.basic_user().email):
            limit_arg = "limit={}".format(limit)
            offset_arg = "offset={}".format(current_offset)
            url = self.url + "?" + limit_arg + "&" + offset_arg
            response = self.client.get(url)
            results = response.data["results"]
            assert limit == len(results)

            assert response.data["previous"] is not None
            assert "offset" not in response.data["previous"]

            assert limit_arg in response.data["next"]
            next_offset_arg = "offset={}".format(current_offset + limit)
            assert next_offset_arg in response.data["next"]

    def test_get_pagination_attrs_for_offset_in_the_middle(self):
        limit = 4
        current_offset = limit + 2
        for _ in range(current_offset + limit + 2):
            UserContext()
        with self.login(email=self.basic_user().email):
            limit_arg = "limit={}".format(limit)
            offset_arg = "offset={}".format(current_offset)
            url = self.url + "?" + limit_arg + "&" + offset_arg
            response = self.client.get(url)
            results = response.data["results"]
            assert limit == len(results)

            prev_offset_arg = "offset={}".format(current_offset - limit)
            assert prev_offset_arg in response.data["previous"]

            assert limit_arg in response.data["next"]
            next_offset_arg = "offset={}".format(current_offset + limit)
            assert next_offset_arg in response.data["next"]

    def test_get_pagination_attrs_for_offset_between_count_and_limit(self):
        limit = 4
        for _ in range(limit * 5):
            UserContext()
        current_offset = User.objects.count() - limit + 2
        with self.login(email=self.basic_user().email):
            limit_arg = "limit={}".format(limit)
            offset_arg = "offset={}".format(current_offset)
            url = self.url + "?" + limit_arg + "&" + offset_arg
            response = self.client.get(url)
            results = response.data["results"]
            assert limit > len(results)
            assert len(results) == response.data["count"] - current_offset

            prev_offset_arg = "offset={}".format(current_offset - limit)
            assert prev_offset_arg in response.data["previous"]

            assert response.data["next"] is None

    def test_get_pagination_attrs_for_offset_equals_number_of_results(self):
        limit = 4
        for _ in range(limit * 5):
            UserContext()
        with self.login(email=self.basic_user().email):
            current_offset = User.objects.count()
            limit_arg = "limit={}".format(limit)
            offset_arg = "offset={}".format(current_offset)
            url = self.url + "?" + limit_arg + "&" + offset_arg

            response = self.client.get(url)
            results = response.data["results"]
            assert len(results) == 0

            prev_offset_arg = "offset={}".format(current_offset - limit)
            assert prev_offset_arg in response.data["previous"]

            assert response.data["next"] is None

    def test_get_pagination_attrs_for_offset_greater_than_num_of_results(self):
        limit = 4
        for _ in range(limit * 5):
            UserContext()
        with self.login(email=self.basic_user().email):
            count = User.objects.count()
            current_offset = count + 1
            limit_arg = "limit={}".format(limit)
            offset_arg = "offset={}".format(current_offset)
            url = self.url + "?" + limit_arg + "&" + offset_arg
            response = self.client.get(url)
            results = response.data["results"]
            assert len(results) == 0

            prev_offset_arg = "offset={}".format(count - limit)
            assert prev_offset_arg in response.data["previous"]

            assert response.data["next"] is None

    def test_get_pagination_attrs_for_limit_greater_than_num_of_results(self):
        for _ in range(5):
            UserContext()
        with self.login(email=self.basic_user().email):
            count = User.objects.count()
            assert count < DEFAULT_MAX_LIMIT
            limit_arg = "limit={}".format(count + 1)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            results = response.data["results"]
            assert len(results) == count
            assert response.data["previous"] is None
            assert response.data["next"] is None

    def test_get_limit_is_greater_than_max_limit_return_error(self):
        with self.login(email=self.basic_user().email):
            limit = DEFAULT_MAX_LIMIT + 1
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            assert response.status_code == 401
            assert GREATER_THAN_MAX_LIMIT_ERROR.format(
                DEFAULT_MAX_LIMIT) in response.data

    def test_get_limit_is_explicitly_null_return_error(self):
        with self.login(email=self.basic_user().email):
            limit = ''
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_NOT_INTEGER_ERROR.format("limit")
            assert error_msg in response.data

    def test_get_limit_is_non_integer_return_error(self):
        with self.login(email=self.basic_user().email):
            limit = '5.5'
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_NOT_INTEGER_ERROR.format("limit")
            assert error_msg in response.data

    def test_get_limit_is_zero_returns_error(self):
        with self.login(email=self.basic_user().email):
            limit = '0'
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_IS_NON_POSITIVE_ERROR.format("limit")
            assert error_msg in response.data

    def test_get_limit_is_negative_returns_error(self):
        with self.login(email=self.basic_user().email):
            limit = '-1'
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_IS_NON_POSITIVE_ERROR.format("limit")
            assert error_msg in response.data

    def test_get_offset_is_negative_returns_error(self):
        with self.login(email=self.basic_user().email):
            offset = '-1'
            offset_arg = "offset={}".format(offset)
            url = self.url + "?" + offset_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_IS_NEGATIVE_ERROR.format("offset")
            assert error_msg in response.data

    def test_get_offset_is_empty_returns_error(self):
        with self.login(email=self.basic_user().email):
            offset = ''
            offset_arg = "offset={}".format(offset)
            url = self.url + "?" + offset_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_NOT_INTEGER_ERROR.format("offset")
            assert error_msg in response.data

    def test_get_offset_is_non_integer_returns_error(self):
        with self.login(email=self.basic_user().email):
            offset = '5.5'
            offset_arg = "offset={}".format(offset)
            url = self.url + "?" + offset_arg
            response = self.client.get(url)
            assert response.status_code == 401
            error_msg = KWARG_VALUE_NOT_INTEGER_ERROR.format("offset")
            assert error_msg in response.data

    def test_get_offset_is_explicit_zero_returns_successfully(self):
        with self.login(email=self.basic_user().email):
            offset = '0'
            offset_arg = "offset={}".format(offset)
            url = self.url + "?" + offset_arg
            response = self.client.get(url)
            assert response.status_code == 200
            implicit_zero_response = self.client.get(self.url)
            assert response.data == implicit_zero_response.data

    def test_get_adjacent_offsets_has_unique_users(self):
        limit = 3
        for _ in range(limit * 3):
            UserContext()
        with self.login(email=self.basic_user().email):
            limit_arg = "limit={}".format(limit)
            url = self.url + "?" + limit_arg
            response = self.client.get(url)
            first_page_results = response.data["results"]
            next_url = response.data["next"]
            next_response = self.client.get(next_url)
            second_page_results = next_response.data["results"]
            first_page_ids = {result["id"] for result in first_page_results}
            second_page_ids = {result["id"] for result in second_page_results}
            assert not first_page_ids.intersection(second_page_ids)

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(ENTREPRENEUR_GET_FIELDS, get_options)
            assert_fields(EXPERT_GET_FIELDS, get_options)
            post_options = response.data["actions"]["POST"]["properties"]
            assert_fields_required(REQUIRED_POST_FIELDS, post_options)
            assert_fields_not_required(ALL_POST_FIELDS - REQUIRED_POST_FIELDS,
                                       post_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):
            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))

    def test_post_entrepreneur(self):
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, EXAMPLE_ENTREPRENEUR)
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_ENTREPRENEUR["email"]
            assert EntrepreneurProfile.objects.get(user=user)

    def test_post_entrepreneur_with_expert_keys(self):
        with self.login(email=self.basic_user().email):
            data = _example_expert()
            data["user_type"] = EntrepreneurProfile.user_type
            response = self.client.post(self.url, data)
            error_msg = UNSUPPORTED_KEY_ERROR.format(key="company",
                                                     type=data["user_type"])
            assert error_msg in response.data

    def test_post_expert(self):
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, _example_expert())
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_EXPERT["email"]
            assert ExpertProfile.objects.get(user=user)

    def test_post_expert_with_bad_category(self):
        with self.login(email=self.basic_user().email):
            bad_name = "Bad Category"
            response = self.client.post(
                self.url, _example_expert(expert_category=bad_name))
            error_msg = INVALID_CHOICE_ERROR.format(field="expert_category",
                                                    value=bad_name,
                                                    choices=format_choices([]))
            assert error_msg in response.data

    def test_post_expert_with_bad_url(self):
        with self.login(email=self.basic_user().email):
            bad_url = "Bad URL"
            response = self.client.post(
                self.url, _example_expert(personal_website_url=bad_url))
            error_msg = INVALID_URL_ERROR.format(field="personal_website_url",
                                                 value=bad_url)
            assert error_msg in response.data

    def test_post_member(self):
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, EXAMPLE_MEMBER)
            id = response.data["id"]
            user = User.objects.get(id=id)
            assert user.email == EXAMPLE_MEMBER["email"]
            assert MemberProfile.objects.get(user=user)

    def test_post_member_with_bio(self):
        with self.login(email=self.basic_user().email):
            data = {"bio": "I have a bio!"}
            data.update(EXAMPLE_MEMBER)
            response = self.client.post(self.url, data)
            error_msg = UNSUPPORTED_KEY_ERROR.format(key="bio",
                                                     type=data["user_type"])
            assert error_msg in response.data

    def test_post_without_required_field(self):
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, {})
            assert response.status_code == 403

    def test_post_bad_key(self):
        with self.login(email=self.basic_user().email):
            bad_key = "bad key"
            response = self.client.post(self.url, {bad_key: True})
            assert response.status_code == 403
            assert any([bad_key in error for error in response.data])

    def test_post_with_existing_email(self):
        user = UserContext().user
        data = EXAMPLE_MEMBER.copy()
        data["email"] = user.email
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data)
            assert response.status_code == 403
            assert EMAIL_EXISTS_ERROR.format(user.email) in response.data

    def test_updated_at_before_datetime_filter(self):
        updated_none = _user_for_date(None)
        week_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        one_day = datetime.timedelta(days=1)
        updated_before = _user_for_date(week_ago - one_day)
        updated_exactly = _user_for_date(week_ago)
        updated_after = _user_for_date(week_ago + one_day)
        with self.login(email=self.basic_user().email):
            url = "{base_url}?updated_at.before={datestr}".format(
                base_url=self.url,
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
        with self.login(email=self.basic_user().email):
            url = "{base_url}?date_modified__gt={datestr}".format(
                base_url=self.url,
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
