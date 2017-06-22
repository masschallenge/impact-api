# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)
from impact.models import ExpertCategory


class ExpertCategoryFactory(DjangoModelFactory):

    class Meta:
        model = ExpertCategory

    name = Sequence(lambda n: 'Expert Category {0}'.format(n))
