# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import (
    ApplicationPanelAssignment,
)

from .application_factory import ApplicationFactory
from .panel_factory import PanelFactory
from .scenario_factory import ScenarioFactory


class ApplicationPanelAssignmentFactory(DjangoModelFactory):

    class Meta:
        model = ApplicationPanelAssignment

    application = SubFactory(ApplicationFactory)
    panel = SubFactory(PanelFactory)
    scenario = SubFactory(ScenarioFactory)
    panel_slot_number = Sequence(lambda n: n)
    remote_pitch = False
    notes = "test assignment"
