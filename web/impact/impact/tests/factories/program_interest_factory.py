# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import ProgramInterest

from .program_factory import ProgramFactory
from .startup_cycle_interest_factory import (
    StartupCycleInterestFactory
)


class ProgramInterestFactory(DjangoModelFactory):

    class Meta:
        model = ProgramInterest

    program = SubFactory(ProgramFactory)
    cycle_interest = SubFactory(StartupCycleInterestFactory)
    applying = False
    interest_level = ""
