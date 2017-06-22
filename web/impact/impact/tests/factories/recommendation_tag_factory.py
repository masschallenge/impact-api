# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)
from impact.models import RecommendationTag


class RecommendationTagFactory(DjangoModelFactory):

    class Meta:
        model = RecommendationTag

    text = Sequence(lambda n: "tag_{0}".format(n))
