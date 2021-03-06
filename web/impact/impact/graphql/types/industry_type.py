from graphene_django import DjangoObjectType

from accelerator.models.industry import Industry


class IndustryType(DjangoObjectType):
    class Meta:
        model = Industry
        only_fields = ('name',)
