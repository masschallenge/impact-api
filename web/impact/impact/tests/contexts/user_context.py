# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from datetime import timedelta

from django.utils import timezone

from impact.tests.factories import (
    BaseProfileFactory,
    EntrepreneurProfileFactory,
    ExpertProfileFactory,
    IndustryFactory,
    MemberProfileFactory,
    UserFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
)


class UserContext(object):
    def __init__(self,
                 user_type="ENTREPRENEUR",
                 primary_industry=None,
                 additional_industries=None,
                 functional_expertise=None,
                 program_families=[],
                 program=None):
        user = UserFactory(date_joined=(timezone.now() + timedelta(-10)))
        self.user = user
        self.program_families = program_families
        self.baseprofile = BaseProfileFactory(user=user, user_type=user_type)
        self.program = program
        if user_type == "ENTREPRENEUR":
            self.profile = EntrepreneurProfileFactory(
                user=user,
                program_families=self.program_families)
            user.entrepreneurprofile = self.profile
        elif user_type == "EXPERT":
            self.primary_industry = primary_industry or IndustryFactory()
            self.additional_industries = additional_industries or []
            self.functional_expertise = functional_expertise or []
            self.profile = ExpertProfileFactory(
                user=self.user,
                primary_industry=self.primary_industry,
                additional_industries=self.additional_industries,
                functional_expertise=self.functional_expertise,
                program_families=self.program_families)
            user.expertprofile = self.profile
        elif user_type == "MEMBER":
            self.profile = MemberProfileFactory(user=self.user)
            user.memberprofile = self.profile
        if program:
            self.program_role = ProgramRoleFactory(program=self.program)
            self.program_role_grant = ProgramRoleGrantFactory(
                person=self.user,
                program_role=self.program_role)
        user.save()
