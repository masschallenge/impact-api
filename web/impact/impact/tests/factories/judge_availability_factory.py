# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import JudgeAvailability

from .judge_round_commitment_factory import JudgeRoundCommitmentFactory
from .panel_location_factory import PanelLocationFactory
from .panel_time_factory import PanelTimeFactory
from .panel_type_factory import PanelTypeFactory


class JudgeAvailabilityFactory(DjangoModelFactory):

    class Meta:
        model = JudgeAvailability

    commitment = SubFactory(JudgeRoundCommitmentFactory)
    panel_location = SubFactory(PanelLocationFactory)
    panel_time = SubFactory(PanelTimeFactory)
    panel_type = SubFactory(PanelTypeFactory)
    availability_type = "Available"
