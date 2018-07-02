import graphene
from graphene_django import DjangoObjectType

from accelerator.models.expert_profile import ExpertProfile
from impact.graphql.types.industry_type import IndustryType  # noqa: F401
from impact.graphql.types.startup_type import StartupType
from impact.graphql.types.program_family_type import ProgramFamilyType  # noqa: F401, E501
from impact.graphql.types.user_type import UserType  # noqa: F401
from impact.graphql.types.functional_expertise_type import (
    FunctionalExpertiseType  # noqa: F401, E501
)

class ExpertProfileType(DjangoObjectType):
    mentees = graphene.List(StartupType)
    image_url = graphene.String()

    class Meta:
        model = ExpertProfile
        only_fields = (
            'title',
            'company',
            'phone',
            'twitter_handle',
            'linked_in_url',
            'personal_website_url',
            'bio',
            'expert_category',
            'primary_industry',
            'additional_industries',
            'home_program_family',
            'user',
            'functional_expertise',
        )

    def resolve_image_url(self, info, **kwargs):
        return self.image and self.image.url
