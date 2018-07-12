# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from accelerator.tests.contexts import JudgeFeedbackContext
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.views import AllocateApplicationsView


class TestAllocateApplicationsView(APITestCase):
    def test_get(self):
        context = JudgeFeedbackContext()
        judging_round_id = context.judging_round.id
        judge_id = context.judge.id
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round_id, judge_id])
            response = self.client.get(url)
            assert response.status_code == 204
