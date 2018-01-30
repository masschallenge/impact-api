# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import StartupMentorTrackingRecord

from .program_factory import ProgramFactory
from .startup_factory import StartupFactory


class StartupMentorTrackingRecordFactory(DjangoModelFactory):

    class Meta:
        model = StartupMentorTrackingRecord

    startup = SubFactory(StartupFactory)
    program = SubFactory(ProgramFactory)
    notes = Sequence(lambda n: "List of Goals {0}".format(n))
