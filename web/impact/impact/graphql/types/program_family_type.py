from graphene_django import DjangoObjectType

from mc.models import ProgramFamily


class ProgramFamilyType(DjangoObjectType):
    class Meta:
        model = ProgramFamily
        only_fields = ('name',)
