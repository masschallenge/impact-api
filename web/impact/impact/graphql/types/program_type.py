from graphene_django import DjangoObjectType

from accelerator.models import Program
from impact.graphql.types.program_family_type import ProgramFamilyType


class ProgramType(DjangoObjectType):
    class Meta:
        model = Program
