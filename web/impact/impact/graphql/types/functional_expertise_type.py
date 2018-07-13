from graphene_django import DjangoObjectType
from accelerator.models.functional_expertise import FunctionalExpertise


class FunctionalExpertiseType(DjangoObjectType):
    class Meta:
        model = FunctionalExpertise
        only_fields = ('name')
