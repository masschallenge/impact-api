# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.contrib.auth import get_user_model
from django.urls import reverse

from impact.tests.contexts import UserContext
from impact.tests.factories import (
    ExpertCategoryFactory,
    IndustryFactory,
    MentoringSpecialtiesFactory,
    ProgramFamilyFactory,
)
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import (
    assert_fields,
    assert_fields_missing,
    assert_fields_not_required,
    assert_fields_required,
)
from impact.utils import get_profile
from impact.v1.helpers import (
    INVALID_ID_ERROR,
    MISSING_SUBJECT_ERROR,
    UserHelper,
    VALID_KEYS_NOTE,
)
from impact.models.base_profile import (
    BASE_ENTREPRENEUR_TYPE,
    BASE_EXPERT_TYPE,
    BASE_MEMBER_TYPE,
    PHONE_MAX_LENGTH,
    TWITTER_HANDLE_MAX_LENGTH,
)
from impact.v1.views.user_detail_view import (
    MISSING_PROFILE_ERROR,
    NO_USER_ERROR,
    UserDetailView,
)

DATE_FIELDS = [
    "date_joined",
    "last_login",
    "updated_at",
]

WRITE_ONCE_FIELDS = [
    "user_type",
]

NON_PATCH_FIELDS = DATE_FIELDS + WRITE_ONCE_FIELDS

MUTABLE_FIELDS = [
    "email",
    "is_active",
    "facebook_url",
    "gender",
    "linked_in_url",
    "personal_website_url",
    "phone",
    "twitter_handle",
]

NON_MEMBER_MUTABLE_FIELDS = ["bio"]

ENTREPRENEUR_PATCH_FIELDS = MUTABLE_FIELDS + NON_MEMBER_MUTABLE_FIELDS
ENTREPRENEUR_GET_FIELDS = (DATE_FIELDS +
                           ENTREPRENEUR_PATCH_FIELDS +
                           WRITE_ONCE_FIELDS)

EXPERT_ONLY_MUTABLE_FIELDS = [
    "company",
    "expert_category",
    "home_program_family_id",
    "judge_interest",
    "mentor_interest",
    "office_hours_interest",
    "office_hours_topics",
    "primary_industry_id",
    "referred_by",
    "speaker_interest",
    "speaker_topics",
    "title",
]

EXPERT_READ_ONLY_FIELDS = [
    "additional_industry_ids",
    "mentoring_specialties",
]

EXPERT_MUTABLE_FIELDS = EXPERT_ONLY_MUTABLE_FIELDS + NON_MEMBER_MUTABLE_FIELDS
EXPERT_ONLY_FIELDS = EXPERT_ONLY_MUTABLE_FIELDS + EXPERT_READ_ONLY_FIELDS

User = get_user_model()


class TestUserDetailView(APITestCase):
    def test_get(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.get(url)
            assert user.first_name == response.data["first_name"]
            assert user.last_name == response.data["last_name"]
            assert user.last_login == response.data.get("last_login")
            assert user.date_joined == response.data["date_joined"]
            helper = UserHelper(user)
            assert helper.field_value("phone") == response.data["phone"]
            assert (helper.field_value("user_type") ==
                    response.data["user_type"])

    def test_get_expert_fields(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        profile = context.profile
        category = profile.expert_category
        specialty = MentoringSpecialtiesFactory()
        profile.mentoring_specialties.add(specialty)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.get(url)
            assert category.name == response.data["expert_category"]
            assert specialty.name in response.data["mentoring_specialties"]

    def test_get_expert_with_industries(self):
        primary_industry = IndustryFactory()
        additional_industries = IndustryFactory.create_batch(2)
        context = UserContext(user_type=BASE_EXPERT_TYPE,
                              primary_industry=primary_industry,
                              additional_industries=additional_industries)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.get(url)
            assert response.data["primary_industry_id"] == primary_industry.id
            assert all([industry.id in response.data["additional_industry_ids"]
                        for industry in additional_industries])

    def test_get_with_no_profile(self):
        context = UserContext(user_type=BASE_ENTREPRENEUR_TYPE)
        user = context.user
        user.entrepreneurprofile.delete()
        user.entrepreneurprofile = None
        user.save()
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.get(url)
            assert user.first_name == response.data["first_name"]
            assert user.last_name == response.data["last_name"]
            assert user.last_login == response.data.get("last_login")
            assert user.date_joined == response.data["date_joined"]
            assert "phone" not in response.data

    def test_options(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_data = response.data["actions"]["GET"]
            assert get_data["type"] == "object"
            get_options = get_data["properties"]
            assert_fields(ENTREPRENEUR_GET_FIELDS, get_options)
            assert_fields_missing(EXPERT_ONLY_FIELDS, get_options)
            patch_options = response.data["actions"]["PATCH"]["properties"]
            assert_fields_required(["id"], patch_options)
            assert_fields_not_required(ENTREPRENEUR_PATCH_FIELDS,
                                       patch_options)
            assert_fields_missing(NON_PATCH_FIELDS, patch_options)
            assert_fields_missing(EXPERT_ONLY_FIELDS, patch_options)
            assert_fields_missing(["POST"], response.data["actions"])

    def test_expert_options(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.options(url)
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields(EXPERT_ONLY_FIELDS, get_options)
            patch_options = response.data["actions"]["PATCH"]["properties"]
            assert_fields(EXPERT_ONLY_MUTABLE_FIELDS, patch_options)

    def test_member_options(self):
        context = UserContext(user_type=BASE_MEMBER_TYPE)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.options(url)
            get_options = response.data["actions"]["GET"]["properties"]
            assert_fields_missing(NON_MEMBER_MUTABLE_FIELDS, get_options)
            patch_options = response.data["actions"]["PATCH"]["properties"]
            assert_fields_missing(NON_MEMBER_MUTABLE_FIELDS, patch_options)

    def test_options_against_get(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))

    def test_patch(self):
        context = UserContext()
        user = context.user
        profile = get_profile(user)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bio = profile.bio + " I'm an awesome API!"
            email = user.email + ".org"
            facebook_url = profile.facebook_url + "/awesome"
            first_name = "Awesome"
            is_active = not user.is_active
            linked_in_url = profile.linked_in_url + "/awesome"
            website_url = profile.personal_website_url + "/awesome"
            phone = "+1-555-555-1234"
            twitter_handle = "@awesome"
            data = {
                "bio": bio,
                "email": email,
                "facebook_url": facebook_url,
                "first_name": first_name,
                "gender": "Male",
                "is_active": is_active,
                "linked_in_url": linked_in_url,
                "personal_website_url": website_url,
                "phone": phone,
                "twitter_handle": twitter_handle,
            }
            response = self.client.patch(url, data)
            assert response.status_code == 204
            user.refresh_from_db()
            profile.refresh_from_db()
            assert user.email == email
            assert user.first_name == first_name
            assert user.is_active == is_active
            helper = UserHelper(user)
            assert helper.field_value("bio") == bio
            assert helper.field_value("facebook_url") == facebook_url
            assert helper.field_value("gender") == "m"
            assert helper.field_value("linked_in_url") == linked_in_url
            assert helper.field_value("personal_website_url") == website_url
            assert helper.field_value("phone") == phone
            assert helper.field_value("twitter_handle") == twitter_handle

    def test_patch_bad_id(self):
        with self.login(email=self.basic_user().email):
            highest_user = User.objects.order_by("-id").first()
            _id = highest_user.id + 1
            assert not User.objects.filter(id=_id).exists()
            url = reverse(UserDetailView.view_name, args=[_id])
            response = self.client.patch(url, {})
            assert response.status_code == 404
            assert response.data == NO_USER_ERROR.format(_id)

    def test_patch_expert_fields(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        profile = get_profile(user)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            company = profile.company + ", Inc."
            expert_category = ExpertCategoryFactory().name
            title = "Chief " + profile.title
            office_hours_topics = "Fungi"
            referred_by = "me"
            speaker_topics = "Fungi"
            data = {
                "company": company,
                "expert_category": expert_category,
                "title": title,
                "office_hours_interest": True,
                "office_hours_topics": office_hours_topics,
                "referred_by": referred_by,
                "speaker_interest": True,
                "speaker_topics": speaker_topics,
                "judge_interest": False,
                "mentor_interest": True,
            }
            self.client.patch(url, data)
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert helper.field_value("company") == company
            assert helper.field_value("expert_category") == expert_category
            assert helper.field_value("title") == title
            assert (helper.field_value("office_hours_interest") is True)
            assert (helper.field_value("office_hours_topics") ==
                    office_hours_topics)
            assert helper.field_value("referred_by") == referred_by
            assert helper.field_value("speaker_interest") is True
            assert helper.field_value("speaker_topics") == speaker_topics
            assert helper.field_value("judge_interest") is False
            assert helper.field_value("mentor_interest") is True

    def test_patch_personal_website_url_with_email_and_password_url(self):
        context = UserContext(user_type=BASE_ENTREPRENEUR_TYPE)
        user = context.user
        profile = get_profile(user)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            website_url = "http://usuario:LINGO321@beta.lingofante.com/demo/"
            data = {
                "personal_website_url": website_url,
            }
            self.client.patch(url, data)
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert helper.field_value("personal_website_url") == website_url

    def test_patch_expert_field_fails_for_entrepreneur(self):
        context = UserContext(user_type=BASE_ENTREPRENEUR_TYPE)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            data = {
                "company": "iStrtupify",
            }
            response = self.client.patch(url, data)
            assert response.status_code == 403
            valid_note = _valid_note(response.data)
            assert "company" not in valid_note
            assert "bio" in valid_note

    def test_patch_bio_fails_for_member(self):
        context = UserContext(user_type=BASE_MEMBER_TYPE)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bio = "I'm an awesome API!"
            data = {
                "bio": bio,
            }
            response = self.client.patch(url, data)
            assert response.status_code == 403
            valid_note = _valid_note(response.data)
            assert "bio" not in valid_note
            assert "first_name" in valid_note

    def test_patch_invalid_key(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "bad key"
            response = self.client.patch(url, {bad_value: True})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_gender(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "bad gender"
            response = self.client.patch(url, {"gender": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_twitter_handle(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "a" * (TWITTER_HANDLE_MAX_LENGTH + 1)
            response = self.client.patch(url, {"twitter_handle": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_boolean(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "Maybe"
            response = self.client.patch(url, {"is_active": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_phone_string(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "Call me!"
            response = self.client.patch(url, {"phone": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_phone_too_long(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "5" * (PHONE_MAX_LENGTH + 1)
            response = self.client.patch(url, {"phone": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_email(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "This is *not* a valid email"
            response = self.client.patch(url, {"email": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_url(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "This is *not* a valid url"
            response = self.client.patch(url,
                                         {"facebook_url": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_no_duplicate_error_msg(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "This is *not* a valid url"
            response = self.client.patch(url,
                                         {"facebook_url": bad_value,
                                          "phone": "1234567890"})
            assert response.status_code == 403
            assert len(response.data) == len(set(response.data))
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_personal_website_url(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = "This is *not* a valid url"
            response = self.client.patch(url,
                                         {"personal_website_url": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_ids(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        profile = get_profile(user)
        industry = IndustryFactory()
        program_family = ProgramFamilyFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            self.client.patch(url, {
                "home_program_family_id": program_family.id,
                "primary_industry_id": industry.id,
            })
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert (helper.field_value("home_program_family_id") ==
                    program_family.id)
            assert helper.field_value("primary_industry_id") == industry.id

    def test_patch_blank_url(self):
        context = UserContext()
        user = context.user
        profile = get_profile(user)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            empty_value = ""
            self.client.patch(url, {"facebook_url": empty_value})
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert helper.field_value("facebook_url") == empty_value

    def test_patch_blank_phone(self):
        context = UserContext()
        user = context.user
        profile = get_profile(user)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            empty_value = ""
            self.client.patch(url, {"phone": empty_value})
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert helper.field_value("phone") == empty_value

    def test_patch_blank_twitter_handle(self):
        context = UserContext()
        user = context.user
        profile = get_profile(user)
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            empty_value = ""
            self.client.patch(url, {"twitter_handle": empty_value})
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert helper.field_value("twitter_handle") == empty_value

    def test_patch_invalid_primary_industry_id(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            bad_value = 0
            response = self.client.patch(url, {
                "home_program_family_id": bad_value,
                "primary_industry_id": bad_value,
            })
            assert response.status_code == 403
            error_msg = INVALID_ID_ERROR.format(
                field="home_program_family_id",
                classname="ProgramFamily")
            assert error_msg in response.data
            error_msg = INVALID_ID_ERROR.format(
                field="primary_industry_id",
                classname="Industry")
            assert error_msg in response.data
            assert "home_program_family_id" in _valid_note(response.data)

    def test_patch_with_no_profile(self):
        context = UserContext(user_type=BASE_ENTREPRENEUR_TYPE)
        user = context.user
        user.entrepreneurprofile.delete()
        user.entrepreneurprofile = None
        user.save()
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            new_last_name = user.last_name + ", Jr."
            response = self.client.patch(url, {"last_name": new_last_name})
            assert response.status_code == 204
            user.refresh_from_db()
            assert user.last_name == new_last_name

    def test_patch_user_with_no_profile_not_allowed_on_missing_fields(self):
        context = UserContext(user_type=BASE_ENTREPRENEUR_TYPE)
        user = context.user
        user.entrepreneurprofile.delete()
        user.entrepreneurprofile = None
        user.save()
        with self.login(email=self.basic_user().email):
            url = reverse(UserDetailView.view_name, args=[user.id])
            response = self.client.patch(url, {"personal_website_url": ""})
            assert response.status_code == 403
            assert MISSING_PROFILE_ERROR.format(user.id) in response.data
            assert MISSING_SUBJECT_ERROR in response.data


def _valid_note(messages):
    note_prefix = VALID_KEYS_NOTE.format("")
    for msg in messages:
        if msg.startswith(note_prefix):
            return msg
    return ""
