# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)
from accelerator.models import StartupRole


class StartupRoleFactory(DjangoModelFactory):

    class Meta:
        model = StartupRole

    name = Sequence(lambda x: "StartupRole %d" % x)
