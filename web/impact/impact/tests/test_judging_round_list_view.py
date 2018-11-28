# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from django.conf import settings

from accelerator.models import (
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    IN_PERSON_JUDGING_ROUND_TYPE,
    ONLINE_JUDGING_ROUND_TYPE,
)
from accelerator.tests.factories.clearance_factory import ClearanceFactory
from impact.tests.factories import JudgingRoundFactory
from impact.tests.api_test_case import APITestCase
from impact.tests.test_judging_round_detail_view import (
    JUDGING_ROUND_GET_FIELDS,
)
from impact.tests.utils import assert_fields
from impact.v1.views import (
    INVALID_IS_ACTIVE_ERROR,
    INVALID_ROUND_TYPE_ERROR,
    JudgingRoundListView,
)


class TestJudgingRoundListView(APITestCase):
    url = reverse(JudgingRoundListView.view_name)

    def test_get(self):
        count = 5
        judging_rounds = JudgingRoundFactory.create_batch(count)
        user = self.basic_user()
        for judging_round in judging_rounds:
            _add_clearance(user, judging_round)
        with self.login(email=user.email):
            response = self.client.get(self.url)
            assert response.data["count"] == count
            assert all([JudgingRoundListView.serialize(judging_round)
                        in response.data["results"]
                        for judging_round in judging_rounds])

    def test_get_implicit_pagination(self):
        count = 15
        judging_rounds = JudgingRoundFactory.create_batch(count)
        user = self.basic_user()
        default_pagination_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        for judging_round in judging_rounds:
            _add_clearance(user, judging_round)
        with self.login(email=user.email):
            response = self.client.get(self.url)
            assert len(response.data["results"]) == default_pagination_size

    def test_get_limit_lifted(self):
        count = 15
        judging_rounds = JudgingRoundFactory.create_batch(count)
        user = self.basic_user()
        for judging_round in judging_rounds:
            _add_clearance(user, judging_round)
        with self.login(email=user.email):
            response = self.client.get("%s?limit=all" % self.url)
            assert response.data["count"] == count
            assert all([JudgingRoundListView.serialize(judging_round)
                        in response.data["results"]
                        for judging_round in judging_rounds])

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(JUDGING_ROUND_GET_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):

            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))

    def test_get_is_active(self):
        active_judging_round = JudgingRoundFactory.create(is_active=True)
        inactive_judging_round = JudgingRoundFactory.create(is_active=False)
        user = self.basic_user()
        _add_clearance(user, active_judging_round)
        _add_clearance(user, inactive_judging_round)
        with self.login(email=user.email):
            all_response = self.client.get(self.url)
            all_results = all_response.data["results"]
            active_response = self.client.get(self.url + "?is_active=True")
            active_results = active_response.data["results"]
            assert len(active_results) < len(all_results)
            active_ids = [item["id"] for item in active_results]
            assert active_judging_round.id in active_ids
            assert inactive_judging_round.id not in active_ids

    def test_get_is_active_can_be_lower_case(self):
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url + "?is_active=false")
            assert response.status_code == 200

    def test_get_is_active_cannot_be_bogus(self):
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url + "?is_active=bogus")
            assert response.status_code == 401
            assert response.data == [INVALID_IS_ACTIVE_ERROR.format("bogus")]

    def test_get_by_round_type(self):
        online = JudgingRoundFactory.create(
            round_type=ONLINE_JUDGING_ROUND_TYPE)
        in_person = JudgingRoundFactory.create(
            round_type=IN_PERSON_JUDGING_ROUND_TYPE)
        user = self.basic_user()
        _add_clearance(user, online)
        _add_clearance(user, in_person)
        with self.login(email=user.email):
            all_response = self.client.get(self.url)
            all_results = all_response.data["results"]
            online_response = self.client.get(
                self.url + "?round_type={}".format(ONLINE_JUDGING_ROUND_TYPE))
            online_results = online_response.data["results"]
            assert len(online_results) < len(all_results)
            online_ids = [item["id"] for item in online_results]
            assert online.id in online_ids
            assert in_person.id not in online_ids

    def test_get_round_type_cannot_be_bogus(self):
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url + "?round_type=bogus")
            assert response.status_code == 401
            assert response.data == [INVALID_ROUND_TYPE_ERROR.format("bogus")]

    def test_dont_show_to_user_without_clearance(self):
        the_round = JudgingRoundFactory.create(
            round_type=ONLINE_JUDGING_ROUND_TYPE)
        url = self.url + "?round_type={}".format(ONLINE_JUDGING_ROUND_TYPE)
        user = self.basic_user()
        # User doesn't have clearance for the JudgingRound's ProgramFamily
        with self.login(email=user.email):
            response = self.client.get(url)
            results = response.data["results"]
            round_ids = [item["id"] for item in results]
            self.assertFalse(the_round.id in round_ids)

    def test_do_show_to_user_with_clearance(self):
        the_round = JudgingRoundFactory.create(
            round_type=ONLINE_JUDGING_ROUND_TYPE)
        url = self.url + "?round_type={}".format(ONLINE_JUDGING_ROUND_TYPE)
        user = self.basic_user()
        # Give user clearance for JudgingRound's ProgramFamily
        _add_clearance(user, the_round)
        with self.login(email=user.email):
            response = self.client.get(url)
            results = response.data["results"]
            round_ids = [item["id"] for item in results]
            self.assertTrue(the_round.id in round_ids)

    def test_ignore_clearance_request_param_works(self):
        the_round = JudgingRoundFactory.create(
            round_type=ONLINE_JUDGING_ROUND_TYPE)
        url = self.url + "?round_type={}&ignore_clearance=true".format(
            ONLINE_JUDGING_ROUND_TYPE)
        user = self.basic_user()
        # The user doesn't have clearance, but PF should be displayed anyway
        with self.login(email=user.email):
            response = self.client.get(url)
            results = response.data["results"]
            round_ids = [item["id"] for item in results]
            self.assertTrue(the_round.id in round_ids)

    def test_global_operations_manager_can_view(self):
        count = 5
        judging_rounds = JudgingRoundFactory.create_batch(count)
        user = self.staff_user()
        for judging_round in judging_rounds:
            _add_clearance(user, judging_round)
        with self.login(email=user.email):
            response = self.client.get(self.url)
            assert response.data["count"] == count
            assert all([JudgingRoundListView.serialize(judging_round)
                        in response.data["results"]
                        for judging_round in judging_rounds])


def _add_clearance(user, judging_round):
    ClearanceFactory(level=CLEARANCE_LEVEL_GLOBAL_MANAGER,
                     user=user,
                     program_family=judging_round.program.program_family)
