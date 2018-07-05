# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from accelerator.tests.factories import CriterionOptionSpecFactory

from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_fields
from impact.v1.views import AnalyzeJudgingRoundView


class TestAnalyzeJudgingRoundView(APITestCase):
    def test_get(self):
        option = CriterionOptionSpecFactory()
        judging_round_id = option.criterion.judging_round_id
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[judging_round_id])
            response = self.client.get(url)
            assert len(response.data) == 1
            first_result = response.data["results"][0]
            assert first_result["criterion_option_spec_id"] == option.id

    def test_options(self):
        option = CriterionOptionSpecFactory()
        judging_round_id = option.criterion.judging_round_id
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[judging_round_id])
            response = self.client.options(url)
            assert response.status_code == 200
            get_options = response.data["actions"]["GET"]["properties"]
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(AnalyzeJudgingRoundView.fields().keys(), get_options)

    def test_options_against_get(self):
        option = CriterionOptionSpecFactory()
        judging_round_id = option.criterion.judging_round_id
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[judging_round_id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))

    def test_get_with_implicit_option(self):
        option = CriterionOptionSpecFactory(option="")
        judging_round_id = option.criterion.judging_round_id
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[judging_round_id])
            response = self.client.get(url)
            assert len(response.data) == 1
            first_result = response.data["results"][0]
            assert first_result["criterion_option_spec_id"] == option.id
