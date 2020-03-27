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
    ProgramRoleGrantFactory,
    StartupStatusFactory,
    UserFactory,
)


class UserContext(object):
    def __init__(self,
                 user_type="ENTREPRENEUR",
                 primary_industry=None,
                 additional_industries=None,
                 functional_expertise=None,
                 program_families=None,
                 program_role_names=None,
                 startup_status_names=None):
        self.user = UserFactory(date_joined=(timezone.now() + timedelta(-10)))
        self.program_families = program_families or []
        self.program_role_names = program_role_names or []
        self.startup_status_names = startup_status_names or []
        self.baseprofile = BaseProfileFactory(user=self.user,
                                              user_type=user_type)
        if user_type == "ENTREPRENEUR":
            self.profile = EntrepreneurProfileFactory(
                user=self.user,
                program_families=self.program_families)
            self.user.entrepreneurprofile = self.profile
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
            self.user.expertprofile = self.profile
        elif user_type == "MEMBER":
            self.profile = MemberProfileFactory(user=self.user)
            self.user.memberprofile = self.profile
        self.user.save()
        self.program_role_grants = [
            ProgramRoleGrantFactory(person=self.user,
                                    program_role__user_role__name=role_name)
            for role_name in self.program_role_names]
        self.startup_role_grants = [
            StartupStatusFactory(
                startup__user=self.user,
                program_startup_status__startup_role__name=status_name)
            for status_name in self.startup_status_names]
