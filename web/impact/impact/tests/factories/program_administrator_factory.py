# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)
from accelerator.models import ProgramAdministrator
from .user_factory import UserFactory


class ProgramAdministratorFactory(DjangoModelFactory):

    class Meta:
        model = ProgramAdministrator

    user = SubFactory(UserFactory)
