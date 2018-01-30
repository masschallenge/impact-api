# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from accelerator.models import (
    PanelType,
)

from .judging_round_factory import JudgingRoundFactory


class PanelTypeFactory(DjangoModelFactory):

    class Meta:
        model = PanelType

    panel_type = Sequence(lambda n: "Panel Type {0}".format(n))
    description = Sequence(lambda n: "Panel Type Description {0}".format(n))
    judging_round = SubFactory(JudgingRoundFactory)
