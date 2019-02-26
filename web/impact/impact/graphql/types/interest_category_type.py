from graphene_django import DjangoObjectType

from accelerator.models import InterestCategory


class InterestCategoryType(DjangoObjectType):
    class Meta:
        model = InterestCategory
