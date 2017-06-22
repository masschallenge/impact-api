# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import ExpertInterest

from .expert_factory import ExpertFactory
from .expert_interest_type_factory import ExpertInterestTypeFactory
from .program_family_factory import ProgramFamilyFactory


class ExpertInterestFactory(DjangoModelFactory):

    class Meta:
        model = ExpertInterest

    user = SubFactory(ExpertFactory)
    program_family = SubFactory(ProgramFamilyFactory)
    interest_type = SubFactory(ExpertInterestTypeFactory)
    topics = Sequence(lambda n: "Expert Interest Topic {}".format(n))
