# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import (
    JudgingRoundStage,
)
from impact.tests.utils import months_from_now

from .judging_round_factory import JudgingRoundFactory


class JudgingRoundStageFactory(DjangoModelFactory):

    class Meta:
        model = JudgingRoundStage

    judging_round = SubFactory(JudgingRoundFactory)
    name = Sequence(lambda n: "Judging Round Stage {0}".format(n))
    start_date_time = months_from_now(1)
    end_date_time = months_from_now(2)
    is_active = True
