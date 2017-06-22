# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import (
    COMPLETE_PANEL_ASSIGNMENT_STATUS,
    JudgePanelAssignment,
)

from .expert_factory import ExpertFactory
from .panel_factory import PanelFactory
from .scenario_factory import ScenarioFactory


class JudgePanelAssignmentFactory(DjangoModelFactory):

    class Meta:
        model = JudgePanelAssignment

    judge = SubFactory(ExpertFactory)
    panel = SubFactory(PanelFactory)
    scenario = SubFactory(ScenarioFactory)
    assignment_status = COMPLETE_PANEL_ASSIGNMENT_STATUS
    panel_sequence_number = Sequence(lambda n: n)
