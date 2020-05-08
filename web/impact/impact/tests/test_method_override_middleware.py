# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from .middleware.method_override_middleware import METHOD_OVERRIDE_HEADER
from .tests.api_test_case import APITestCase
from .tests.contexts import UserContext


class TestMethodOverrideMiddleware(APITestCase):

    def test_patch_via_post(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse("user_detail", args=[user.id])
            new_first_name = "David"
            self.client.post(
                url,
                **{METHOD_OVERRIDE_HEADER: "PATCH"},
                data={"first_name": new_first_name})
            user.refresh_from_db()
            assert user.first_name == new_first_name

    def test_patch_via_get_makes_no_change(self):
        context = UserContext()
        user = context.user
        with self.login(email=self.basic_user().email):
            url = reverse("user_detail", args=[user.id])
            new_first_name = "David"
            self.client.get(
                url,
                **{METHOD_OVERRIDE_HEADER: "PATCH"},
                data={"first_name": new_first_name})
            user.refresh_from_db()
            assert user.first_name != new_first_name
