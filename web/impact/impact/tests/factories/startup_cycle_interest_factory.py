# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory
)

from impact.models import StartupCycleInterest

from .program_cycle_factory import ProgramCycleFactory
from .startup_factory import StartupFactory


class StartupCycleInterestFactory(DjangoModelFactory):

    class Meta:
        model = StartupCycleInterest
    cycle = SubFactory(ProgramCycleFactory)
    startup = SubFactory(StartupFactory)
