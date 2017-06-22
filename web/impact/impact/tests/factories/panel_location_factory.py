# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from impact.models import PanelLocation
from .judging_round_factory import JudgingRoundFactory


class PanelLocationFactory(DjangoModelFactory):

    class Meta:
        model = PanelLocation

    location = Sequence(lambda n: "Location {0}".format(n))
    description = Sequence(lambda n: "Panel Location {0}".format(n))
    judging_round = SubFactory(JudgingRoundFactory)
