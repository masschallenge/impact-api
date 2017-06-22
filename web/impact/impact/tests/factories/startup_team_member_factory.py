# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
    post_generation,
)
from impact.models import StartupTeamMember
from .startup_factory import StartupFactory
from .user_factory import UserFactory


class StartupTeamMemberFactory(DjangoModelFactory):

    class Meta:
        model = StartupTeamMember

    startup = SubFactory(StartupFactory)
    user = SubFactory(UserFactory)
    title = Sequence(lambda n: "Title {0}".format(n))
    startup_administrator = False
    primary_contact = False
    technical_contact = False
    marketing_contact = False
    financial_contact = False
    legal_contact = False
    product_contact = False
    design_contact = False
    is_contact = True
    display_on_public_profile = False
    founder = False

    @post_generation
    def recommendation_tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.recommendation_tags.add(tag)
