# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)
from accelerator.models import StartupStatus
from .startup_factory import StartupFactory
from .program_startup_status_factory import ProgramStartupStatusFactory


class StartupStatusFactory(DjangoModelFactory):

    class Meta:
        model = StartupStatus

    startup = SubFactory(StartupFactory)
    program_startup_status = SubFactory(ProgramStartupStatusFactory)
