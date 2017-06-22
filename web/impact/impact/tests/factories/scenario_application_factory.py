# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import (
    ScenarioApplication,
)

from .application_factory import ApplicationFactory
from .scenario_factory import ScenarioFactory


class ScenarioApplicationFactory(DjangoModelFactory):
    class Meta:
        model = ScenarioApplication

    application = SubFactory(ApplicationFactory)
    scenario = SubFactory(ScenarioFactory)
