# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)

from impact.models import ExpertInterestType


class ExpertInterestTypeFactory(DjangoModelFactory):

    class Meta:
        model = ExpertInterestType

    name = Sequence(lambda n: "Expert Interest {}".format(n))
    short_description = Sequence(lambda n: "Description {}".format(n))
