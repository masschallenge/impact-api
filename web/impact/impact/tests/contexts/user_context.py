# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.tests.factories import (
    BaseProfileFactory,
    EntrepreneurProfileFactory,
    ExpertProfileFactory,
    IndustryFactory,
    MemberProfileFactory,
    UserFactory,
)


class UserContext(object):
    def __init__(self,
                 user_type="ENTREPRENEUR",
                 primary_industry=None,
                 additional_industries=None):
        user = UserFactory()
        self.user = user
        self.baseprofile = BaseProfileFactory(user=user, user_type=user_type)
        if user_type == "ENTREPRENEUR":
            self.profile = EntrepreneurProfileFactory(user=user)
            user.entrepreneurprofile = self.profile
        elif user_type == "EXPERT":
            self.primary_industry = primary_industry or IndustryFactory()
            self.additional_industries = additional_industries or []
            self.profile = ExpertProfileFactory(
                user=self.user,
                primary_industry=self.primary_industry,
                additional_industries=self.additional_industries)
            user.expertprofile = self.profile
        elif user_type == "MEMBER":
            self.profile = MemberProfileFactory(user=self.user)
            user.memberprofile = self.profile
        user.save()
