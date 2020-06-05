from graphene_django import DjangoObjectType

from mc.models import InterestCategory


class InterestCategoryType(DjangoObjectType):
    class Meta:
        model = InterestCategory
