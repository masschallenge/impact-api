# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.contexts import UserContext
from impact.tests.factories import MentoringSpecialtiesFactory
from impact.tests.api_test_case import APITestCase
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

    def test_patch(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            is_active = not user.is_active
            first_name = "David"
            phone = "+1-555-555-5555"
            data = {
                "is_active": is_active,
                "first_name": first_name,
                "gender": "Male",
                "phone": phone,
                }
            self.client.patch(url, data)
            user.refresh_from_db()
            assert user.is_active == is_active
            assert user.full_name == first_name
            assert UserHelper(user).field_value("phone") == phone

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
            assert bad_gender in response.data

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
