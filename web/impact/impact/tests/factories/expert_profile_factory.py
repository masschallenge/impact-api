# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    Sequence,
    SubFactory,
    post_generation,
)

from impact.models import ExpertProfile

from .core_profile_factory import CoreProfileFactory
from .expert_category_factory import ExpertCategoryFactory
from .industry_factory import IndustryFactory
from .program_family_factory import ProgramFamilyFactory


class ExpertProfileFactory(CoreProfileFactory):

    class Meta:
        model = ExpertProfile

    salutation = Sequence(lambda x: "Expert Title %d" % x)
    title = Sequence(lambda x: "Expert title %d" % x)
    company = Sequence(lambda x: "Expert Company %d" % x)
    expert_category = SubFactory(ExpertCategoryFactory)
    primary_industry = SubFactory(IndustryFactory)
    privacy_email = "finalists and staff"
    privacy_phone = "finalists and staff"
    privacy_web = "finalists and staff"
    public_website_consent = True
    public_website_consent_checked = True
    judge_interest = False
    mentor_interest = False
    speaker_interest = False
    privacy_policy_accepted = True
    speaker_topics = ""
    office_hours_interest = False
    office_hours_topics = ""
    expert_group = ""
    reliability = None
    referred_by = ""
    other_potential_experts = ""
    internal_notes = ""
    bio = Sequence(lambda x: "Bio text %d" % x)
    home_program_family = SubFactory(ProgramFamilyFactory)

    @post_generation
    def functional_expertise(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for expertise in extracted:
                self.functional_expertise.add(expertise)

    @post_generation
    def additional_industries(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for industry in extracted:
                self.additional_industries.add(industry)

    @post_generation
    def mentoring_specialties(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for specialty in extracted:
                self.mentoring_specialties.add(specialty)
