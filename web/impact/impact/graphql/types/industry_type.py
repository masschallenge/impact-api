from graphene_django import DjangoObjectType

from mc.models import Industry


class IndustryType(DjangoObjectType):
    class Meta:
        model = Industry
        only_fields = ('name',)
