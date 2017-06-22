# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import StartupProgramInterest

from .program_factory import ProgramFactory
from .startup_factory import StartupFactory


class StartupProgramInterestFactory(DjangoModelFactory):

    class Meta:
        model = StartupProgramInterest

    program = SubFactory(ProgramFactory)
    startup = SubFactory(StartupFactory)
    applying = False
    interest_level = ""
    order = Sequence(lambda n: n)
