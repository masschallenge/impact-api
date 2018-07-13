from graphene_django import DjangoObjectType

from accelerator.models import Program
from impact.graphql.types.program_family_type import ProgramFamilyType  # noqa: F401, E501


class ProgramType(DjangoObjectType):
    class Meta:
        model = Program
