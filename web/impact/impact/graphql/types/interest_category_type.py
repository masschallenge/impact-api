from graphene_django import DjangoObjectType

from accelerator.models import InterestCategory

from impact.graphql.types.program_type import ProgramType  # noqa: F401


class InterestCategoryType(DjangoObjectType):
    class Meta:
        model = InterestCategory
