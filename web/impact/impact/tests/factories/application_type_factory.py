# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import ApplicationType

from .startup_label_factory import StartupLabelFactory


class ApplicationTypeFactory(DjangoModelFactory):

    class Meta:
        model = ApplicationType

    name = Sequence(lambda n: "Application Type {0}".format(n))
    description = Sequence(lambda n:
                           "Application Type Description {0}".format(n))
    submission_label = SubFactory(StartupLabelFactory)
