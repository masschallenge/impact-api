# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import RelatedFactory

from .user_factory import UserFactory
from .base_profile_factory import BaseProfileFactory
from .entrepreneur_profile_factory import EntrepreneurProfileFactory


class EntrepreneurFactory(UserFactory):
    baseprofile = RelatedFactory(BaseProfileFactory, "user")
    profile = RelatedFactory(EntrepreneurProfileFactory, "user")
