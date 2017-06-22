# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from datetime import timedelta
from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import PanelTime
from impact.tests.utils import months_from_now

from .judging_round_factory import JudgingRoundFactory


class PanelTimeFactory(DjangoModelFactory):

    class Meta:
        model = PanelTime

    start_date_time = months_from_now(1)
    end_date_time = months_from_now(1) + timedelta(hours=2)
    day = start_date_time.strftime("%A %-m/%-d")
    time = start_date_time.strftime("%I:%M%p")
    judging_round = SubFactory(JudgingRoundFactory)
