# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import EntrepreneurProfile
from .core_profile_factory import CoreProfileFactory


class EntrepreneurProfileFactory(CoreProfileFactory):
    privacy_policy_accepted = True

    class Meta:
        model = EntrepreneurProfile

    bio = "I was born at a very young age..."
