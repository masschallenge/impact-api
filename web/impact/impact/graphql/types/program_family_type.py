from graphene_django import DjangoObjectType

from accelerator.models.program_family import ProgramFamily


class ProgramFamilyType(DjangoObjectType):
    class Meta:
        model = ProgramFamily
        only_fields = ('name',)
