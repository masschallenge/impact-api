# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import StartupAttribute

from .program_startup_attribute_factory import (
    ProgramStartupAttributeFactory,
)
from .startup_factory import StartupFactory


class StartupAttributeFactory(DjangoModelFactory):

    class Meta:
        model = StartupAttribute

    startup = SubFactory(StartupFactory)
    attribute = SubFactory(ProgramStartupAttributeFactory)
    attribute_value = Sequence(lambda n: "Attribute Value {0}".format(n))
