# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from accelerator.models import (
    JudgeRoundCommitment,
)

from .expert_factory import ExpertFactory
from .judging_round_factory import JudgingRoundFactory


class JudgeRoundCommitmentFactory(DjangoModelFactory):

    class Meta:
        model = JudgeRoundCommitment

    judge = SubFactory(ExpertFactory)
    judging_round = SubFactory(JudgingRoundFactory)
    commitment_state = True
    capacity = 10
    current_quota = 10
