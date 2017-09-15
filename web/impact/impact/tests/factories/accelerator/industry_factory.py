# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import DjangoModelFactory
from accelerator.models import Industry


class IndustryFactory(DjangoModelFactory):

    class Meta:
        model = Industry
