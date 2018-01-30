# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from accelerator.models import BaseProfile

from .user_factory import UserFactory


class BaseProfileFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    user_type = "ENTREPRENEUR"
    privacy_policy_accepted = True

    class Meta:
        model = BaseProfile
