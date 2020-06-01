from graphene_django import DjangoObjectType
from mc.models import FunctionalExpertise


class FunctionalExpertiseType(DjangoObjectType):
    class Meta:
        model = FunctionalExpertise
        only_fields = ('name',)
