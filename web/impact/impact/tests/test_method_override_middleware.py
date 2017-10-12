# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.middleware.method_override_middleware import METHOD_OVERRIDE_HEADER
from impact.tests.api_test_case import APITestCase
from impact.tests.contexts import UserContext


class TestMethodOverrideMiddleware(APITestCase):

    def test_patch(self):
        context = UserContext()
        user = context.user
        with self.login(username=self.basic_user().username):
            url = reverse("user_detail", args=[user.id])
            new_first_name = "David"
            response = self.client.post(
                url,
                headers={'X-HTTP-Method-Override': 'PATCH'},
                data={"first_name": new_first_name},
                follow=True)
            user.refresh_from_db()
            assert user.full_name == new_first_name
