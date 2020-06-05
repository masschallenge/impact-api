# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json

from django.urls import reverse

from accelerator.tests.contexts import AnalyzeJudgingContext
from .api_test_case import APITestCase
from .utils import assert_fields
from ..v1.views import JudgingRoundCriteriaHeaderView


class TestJudgingRoundCriteriaHeaderView(APITestCase):
    view_name = JudgingRoundCriteriaHeaderView.view_name

    def test_get_judging_round_criteria_header(self):
        context = AnalyzeJudgingContext()
        judging_round_id = context.judging_round.id
        with self.login(email=self.basic_user().email):
            url = reverse(self.view_name,
                          args=[judging_round_id])
            response = self.client.get(url)
            _assert_response_matches_context(response, context)

    def test_options_judging_round_criteria_header(self):
        context = AnalyzeJudgingContext()
        judging_round_id = context.judging_round.id
        with self.login(email=self.basic_user().email):
            url = reverse(self.view_name,
                          args=[judging_round_id])
            response = self.client.options(url)
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(JudgingRoundCriteriaHeaderView.fields().keys(),
                          get_options)

    def test_get_no_reads_criteria_exists(self):
        context = AnalyzeJudgingContext(type="gender",
                                        read_count=0)
        judging_round_id = context.judging_round.id
        with self.login(email=self.basic_user().email):
            url = reverse(self.view_name,
                          args=[judging_round_id])
            response = self.client.get(url)
            _assert_response_matches_context(response, context)


def _assert_response_matches_context(response, context):
    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    judging_round = context.judging_round
    json_response = json.loads(response.content)
    actual_start_time = judging_round.start_date_time.strftime(time_format)
    assert actual_start_time == json_response['start_date_time']
    actual_end_time = judging_round.end_date_time.strftime(time_format)
    assert actual_end_time == json_response['end_date_time']
    assert len(context.applications) == json_response['application_count']
    response_reads_required = json_response['total_reads_required']
    assert context.total_reads_required() == response_reads_required
    assert context.judging_capacity == json_response['judging_capacity']
