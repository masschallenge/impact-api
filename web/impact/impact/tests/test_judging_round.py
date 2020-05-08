# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .tests.api_test_case import APITestCase
from .tests.factories import JudgingRoundFactory


class TestJudgingRound(APITestCase):
    def test_str(self):
        judging_round = JudgingRoundFactory()
        judging_round_string = str(judging_round)
        assert judging_round.name in judging_round_string
        assert str(judging_round.program) in judging_round_string
