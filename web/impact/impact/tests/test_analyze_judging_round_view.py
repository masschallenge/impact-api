# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from accelerator.tests.factories import CriterionOptionSpecFactory
from accelerator.tests.contexts import AnalyzeJudgingContext
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

    def test_get_with_unread_application(self):
        context = AnalyzeJudgingContext(type="reads",
                                        name="reads",
                                        read_count=2,
                                        options=[""])
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[context.judging_round.id])
            response = self.client.get(url)
            assert len(response.data) == 1
            first_result = response.data["results"][0]
            assert (first_result["remaining_needed_reads"] ==
                    context.needed_reads())

    def test_get_with_gender_criterion(self):
        genders = ["f", "m"]
        context = AnalyzeJudgingContext(type="judge",
                                        name="gender",
                                        read_count=1,
                                        options=genders)
        judge_key = context.judge.expertprofile.gender
        dists = _calc_judge_dists(context, judge_key)
        self.assert_option_distributions(context, dists)

    def test_get_with_role_criterion(self):
        roles = ["Executive", "Lawyer", "Investor"]
        context = AnalyzeJudgingContext(type="judge",
                                        name="role",
                                        read_count=1,
                                        options=roles)
        judge_key = context.judge.expertprofile.expert_category.name
        dists = _calc_judge_dists(context, judge_key)
        self.assert_option_distributions(context, dists)

    def test_get_with_industry_criterion(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="industry",
                                        read_count=1,
                                        options=[""])
        judge_key = context.judge.expertprofile.primary_industry.name
        options = _industry_options(context)
        dists = _calc_industry_dists(options, judge_key)
        self.assert_option_distributions(context, dists)

    def test_get_with_program_criterion(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="program",
                                        read_count=1,
                                        options=[""])
        # This is where I gave up and just hard coded it!
        dists = {context.program.program_family.name: {0: 1, 1: 1}}
        self.assert_option_distributions(context, dists)

    def assert_option_distributions(self, context, dists):
        judging_round_id = context.criterion.judging_round.id
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[judging_round_id])
            response = self.client.get(url)
            results = response.data["results"]
            for result in results:
                option = result["option"]
                assert result["needs_distribution"] == dists[option]

    def test_get_with_commitment(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="program",
                                        read_count=1,
                                        options=[""])
        commitment = context.judges[0].judgeroundcommitment_set.first()
        judging_round_id = context.criterion.judging_round.id
        with self.login(email=self.basic_user().email):
            url = reverse(AnalyzeJudgingRoundView.view_name,
                          args=[judging_round_id])
            response = self.client.get(url)
            result = response.data["results"][0]
            assert commitment.capacity == result['total_capacity']
            assert commitment.capacity - 1 == result['remaining_capacity']


def _industry_options(context):
    return [app.startup.primary_industry.name
            for app in context.applications]


def _program_options(context):
    return [_program_for_app(app) for app in context.applications]


def _program_for_app(app):
    spi = app.startup.startupprograminterest_set.filter(
        applying=True).first()
    return spi.program.program_family.name


def _calc_judge_dists(context, judge_key):
    app_count = len(context.applications)
    results = {key: {context.read_count: app_count}
               for key in context.options}
    if judge_key in results:
        results[judge_key] = {
            context.read_count - 1: 1,
            context.read_count: app_count - 1
        }
    return results


def _calc_industry_dists(options, judge_key):
    # Assume each app has it's own Industry due to using factories
    results = {key: {1: 1} for key in options}
    if judge_key in results:
        results[judge_key] = {0: 1}
    return results
