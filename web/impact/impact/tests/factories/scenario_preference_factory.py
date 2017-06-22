# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from impact.models import (
    JUDGE_ENTITY,
    JUDGE_IS_FEMALE,
    MIN_PREFERENCE,
    ScenarioPreference,
)
from .scenario_factory import ScenarioFactory


class ScenarioPreferenceFactory(DjangoModelFactory):
    class Meta:
        model = ScenarioPreference

    scenario = SubFactory(ScenarioFactory)
    priority = Sequence(lambda n: str(n))
    constraint_type = MIN_PREFERENCE
    entity_type = JUDGE_ENTITY
    entity_set = JUDGE_IS_FEMALE
    amount = 1
