# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.middleware.method_override_middleware import METHOD_OVERRIDE_HEADER
from impact.tests.api_test_case import APITestCase
from impact.tests.contexts import UserContext


class TestMethodOverrideMiddleware(APITestCase):

    def test_patch_via_post(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            new_first_name = "David"
            self.client.post(
                url,
                **{METHOD_OVERRIDE_HEADER: "PATCH"},
                data={"first_name": new_first_name})
            user.refresh_from_db()
            assert user.full_name == new_first_name

    def test_patch_via_get_makes_no_change(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            new_first_name = "David"
            self.client.get(
                url,
                **{METHOD_OVERRIDE_HEADER: "PATCH"},
                data={"first_name": new_first_name})
            user.refresh_from_db()
            assert user.full_name != new_first_name
