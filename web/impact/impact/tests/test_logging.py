# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from rest_framework_tracking.models import APIRequestLog

from impact.tests.contexts import UserContext
from impact.tests.api_test_case import APITestCase


class TestLogging(APITestCase):

    def test_user_object_access_is_logged(self):
        context = UserContext()
        target_user = context.user
        requesting_user = self.basic_user()
        with self.login(email=requesting_user.email):
            url = reverse("user_detail", args=[target_user.id])
            self.client.get(url)
            log_entry = APIRequestLog.objects.last()
            self.assertEqual(log_entry.user_id, requesting_user.id)
