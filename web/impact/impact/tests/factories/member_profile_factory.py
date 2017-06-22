# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models import MemberProfile

from .core_profile_factory import CoreProfileFactory


class MemberProfileFactory(CoreProfileFactory):

    class Meta:
        model = MemberProfile
