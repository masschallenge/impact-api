# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import DjangoModelFactory
from accelerator.models import RecommendationTag


class RecommendationTagFactory(DjangoModelFactory):

    class Meta:
        model = RecommendationTag
