# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.contexts import UserContext
from impact.tests.factories import (
    ExpertCategoryFactory,
    IndustryFactory,
    MentoringSpecialtiesFactory,
    ProgramFamilyFactory,
)
from impact.tests.api_test_case import APITestCase
from impact.utils import get_profile
from impact.v1.helpers import (
    INVALID_INDUSTRY_ID_ERROR,
    INVALID_PROGRAM_FAMILY_ID_ERROR,
    UserHelper,
    VALID_KEYS_NOTE,
)
from impact.models.base_profile import (
    BASE_ENTREPRENEUR_TYPE,
    BASE_EXPERT_TYPE,
    BASE_MEMBER_TYPE,
)
from impact.models import User
from impact.v1.views.user_detail_view import NO_USER_ERROR


class TestUserDetailView(APITestCase):

    def test_get(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            response = self.client.get(url)
            assert user.full_name == response.data["first_name"]
            assert user.short_name == response.data["last_name"]
            assert user.last_login == response.data.get("last_login")
            assert user.date_joined == response.data["date_joined"]
            helper = UserHelper(user)
            assert helper.field_value("phone") == response.data["phone"]
            assert (helper.field_value("user_type") ==
                    response.data["user_type"])

    def test_patch(self):
        context = UserContext()
        user = context.user
        profile = get_profile(user)
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
            assert user.full_name == first_name
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
        with self.login(username=self.basic_user().username):
            highest_user = User.objects.order_by("-id").first()
            id = highest_user.id + 1
            url = reverse("user_detail", args=[id])
            response = self.client.patch(url, {})
            assert response.status_code == 404
            assert response.data == NO_USER_ERROR.format(id)

    def test_patch_expert_fields(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        profile = get_profile(user)
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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

    def test_patch_personal_website_url_with_username_and_password_url(self):
        context = UserContext(user_type=BASE_ENTREPRENEUR_TYPE)
        user = context.user
        profile = get_profile(user)
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = "bad key"
            response = self.client.patch(url, {bad_value: True})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_gender(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = "bad gender"
            response = self.client.patch(url, {"gender": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_boolean(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = "Maybe"
            response = self.client.patch(url, {"is_active": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_phone(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = "Call me!"
            response = self.client.patch(url, {"phone": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_email(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = "This is *not* a valid email"
            response = self.client.patch(url, {"email": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_invalid_url(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = "This is *not* a valid url"
            response = self.client.patch(url,
                                         {"facebook_url": bad_value})
            assert response.status_code == 403
            assert any(bad_value in datum
                       for datum in response.data)

    def test_patch_no_duplicate_error_msg(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            empty_value = ""
            self.client.patch(url, {"facebook_url": empty_value})
            user.refresh_from_db()
            profile.refresh_from_db()
            helper = UserHelper(user)
            assert helper.field_value("facebook_url") == empty_value

    def test_patch_invalid_primary_industry_id(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_value = 0
            response = self.client.patch(url, {
                    "home_program_family_id": bad_value,
                    "primary_industry_id": bad_value,
                    })
            assert response.status_code == 403
            error_msg = INVALID_PROGRAM_FAMILY_ID_ERROR.format(
                field="home_program_family_id")
            assert error_msg in response.data
            error_msg = INVALID_INDUSTRY_ID_ERROR.format(
                field="primary_industry_id")
            assert error_msg in response.data
            assert "home_program_family_id" in _valid_note(response.data)

    def test_expert_fields(self):
        context = UserContext(user_type=BASE_EXPERT_TYPE)
        user = context.user
        profile = context.profile
        category = profile.expert_category
        specialty = MentoringSpecialtiesFactory()
        profile.mentoring_specialties.add(specialty)
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
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
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            response = self.client.get(url)
            assert response.data["primary_industry_id"] == primary_industry.id
            assert all([industry.id in response.data["additional_industry_ids"]
                        for industry in additional_industries])


def _valid_note(messages):
    note_prefix = VALID_KEYS_NOTE.format("")
    for msg in messages:
        if msg.startswith(note_prefix):
            return msg
    return ""
