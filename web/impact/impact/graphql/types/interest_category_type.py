import graphene
from graphene_django import DjangoObjectType

from accelerator.models import InterestCategory

from impact.graphql.types.program_type import ProgramType


class InterestCategoryType(DjangoObjectType):
    class Meta:
        model = InterestCategory
