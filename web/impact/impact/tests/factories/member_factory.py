# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import RelatedFactory

from .base_profile_factory import BaseProfileFactory
from .member_profile_factory import MemberProfileFactory
from .user_factory import UserFactory


class MemberFactory(UserFactory):
    baseprofile = RelatedFactory(BaseProfileFactory, "user",
                                 user_type="MEMBER")
    profile = RelatedFactory(MemberProfileFactory, "user")
