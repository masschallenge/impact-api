# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import ScenarioJudge

from .expert_factory import ExpertFactory
from .scenario_factory import ScenarioFactory


class ScenarioJudgeFactory(DjangoModelFactory):
    class Meta:
        model = ScenarioJudge

    # Note: is_judge will not be true after this.
    # To get a real just you need to use a UserRoleContext.
    judge = SubFactory(ExpertFactory)
    scenario = SubFactory(ScenarioFactory)
