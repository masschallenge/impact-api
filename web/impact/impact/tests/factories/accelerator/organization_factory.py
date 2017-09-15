# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory
)

from accelerator.models import Organization


class OrganizationFactory(DjangoModelFactory):

    class Meta:
        model = Organization
