# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import StartupOverrideGrant

from .program_override_factory import ProgramOverrideFactory
from .startup_factory import StartupFactory


class StartupOverrideGrantFactory(DjangoModelFactory):
    class Meta:
        model = StartupOverrideGrant

    startup = SubFactory(StartupFactory)
    program_override = SubFactory(ProgramOverrideFactory)
