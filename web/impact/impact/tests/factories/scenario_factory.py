# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
    post_generation,
)

from accelerator.models import (
    DEFAULT_PANEL_SIZE,
    Scenario,
)

from .judging_round_factory import JudgingRoundFactory


class ScenarioFactory(DjangoModelFactory):
    class Meta:
        model = Scenario

    name = Sequence(lambda n: "Scenario {0}".format(n))
    description = Sequence(lambda n: "Scenario Description {0}".format(n))
    judging_round = SubFactory(JudgingRoundFactory)
    is_active = True
    panel_size = DEFAULT_PANEL_SIZE
    max_panels_per_judge = None
    min_panels_per_judge = 1
    sequence_number = Sequence(lambda n: str(n))

    @post_generation
    def judges(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.judges.add(tag)

    @post_generation
    def applications(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.applications.add(tag)
