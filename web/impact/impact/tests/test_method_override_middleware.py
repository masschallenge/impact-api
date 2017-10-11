# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.tests.api_test_case import APITestCase
from impact.tests.contexts import UserContext
from .method_override_middleware import METHOD_OVERRIDE_HEADER


class TestMethodOverrideMiddleware(APITestCase):

    def test_patch(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            first_name = "David"
            data = {
                "first_name": first_name,
                }
            header = METHOD_OVERRIDE_HEADER
            
            self.client.post(url, data, header)
            user.refresh_from_db()
            assert user.full_name == first_name