# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.contexts import UserContext
from impact.tests.factories import (
    IndustryFactory,
    MentoringSpecialtiesFactory,
)
from impact.tests.api_test_case import APITestCase
from impact.utils import get_profile
from impact.v1.helpers import UserHelper


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
            assert (UserHelper(user).field_value("phone") ==
                    response.data["phone"])
            assert (UserHelper(user).field_value("user_type") ==
                    response.data["user_type"])

    def test_patch(self):
        context = UserContext()
        user = context.user
        profile = get_profile(user)
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            is_active = not user.is_active
            first_name = "David"
            phone = "+1-555-555-1234"
            bio = "I'm an awesome API!"
            data = {
                "is_active": is_active,
                "first_name": first_name,
                "gender": "Male",
                "phone": phone,
                "bio": bio,
                }
            response = self.client.patch(url, data)
            user.refresh_from_db()
            profile.refresh_from_db()
            assert user.is_active == is_active
            assert user.full_name == first_name
            assert UserHelper(user).field_value("gender") == "m"
            assert UserHelper(user).field_value("phone") == phone
            assert UserHelper(user).field_value("bio") == bio

    def test_patch_invalid_key(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_key = "bad key"
            response = self.client.patch(url, {bad_key: True})
            assert response.status_code == 403
            assert bad_key in response.data

    def test_patch_invalid_gender(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            bad_gender = "bad gender"
            response = self.client.patch(url, {"gender": bad_gender})
            assert response.status_code == 403
            assert any(bad_gender in datum
                       for datum in response.data)

    def test_expert_fields(self):
        context = UserContext(user_type="EXPERT")
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
        context = UserContext(user_type="EXPERT",
                              primary_industry=primary_industry,
                              additional_industries=additional_industries)
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            response = self.client.get(url)
            assert response.data["primary_industry_id"] == primary_industry.id
            assert all([industry.id in response.data["additional_industry_ids"]
                        for industry in additional_industries])
