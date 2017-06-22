# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import RelatedFactory

from .user_factory import UserFactory
from .base_profile_factory import BaseProfileFactory
from .expert_profile_factory import ExpertProfileFactory


class ExpertFactory(UserFactory):
    baseprofile = RelatedFactory(BaseProfileFactory, "user",
                                 user_type="EXPERT")
    profile = RelatedFactory(ExpertProfileFactory, "user")
