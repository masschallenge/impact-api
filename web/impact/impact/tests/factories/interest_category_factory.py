# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import InterestCategory

from .program_factory import ProgramFactory


class InterestCategoryFactory(DjangoModelFactory):

    class Meta:
        model = InterestCategory

    name = Sequence(lambda n: "Interest Category {0}".format(n))
    program = SubFactory(ProgramFactory)
