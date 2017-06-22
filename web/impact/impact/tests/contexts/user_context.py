# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.tests.factories import (
    BaseProfileFactory,
    EntrepreneurProfileFactory,
    ExpertProfileFactory,
    MemberProfileFactory,
    UserFactory,
)


class UserContext(object):
    def __init__(self, user_type="ENTREPRENEUR"):
        user = UserFactory()
        self.user = user
        self.baseprofile = BaseProfileFactory(user=user, user_type=user_type)
        if user_type == "ENTREPRENEUR":
            self.profile = EntrepreneurProfileFactory(user=user)
            user.entrepreneurprofile = self.profile
        elif user_type == "EXPERT":
            self.profile = ExpertProfileFactory(user=self.user)
            user.expertprofile = self.profile
        elif user_type == "MEMBER":
            self.profile = MemberProfileFactory(user=self.user)
            user.memberprofile = self.profile
        user.save()
