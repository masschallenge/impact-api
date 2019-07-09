import graphene

from impact.graphql.types import (
    EntrepreneurProfileType,
    ExpertProfileType,
)
from accelerator.models import (
    EntrepreneurProfile,
    ExpertProfile,
)
from graphql import GraphQLError
ENTREPRENEUR_NOT_FOUND_MESSAGE = 'Entrepreneur matching the id does not exist.'
EXPERT_NOT_FOUND_MESSAGE = 'Expert matching the id does not exist.'


class Query(graphene.ObjectType):
    expert_profile = graphene.Field(
        ExpertProfileType, id=graphene.Int())
    entrepreneur_profile = graphene.Field(
        EntrepreneurProfileType, id=graphene.Int())

    def resolve_expert_profile(self, info, **kwargs):
        user_id = kwargs.get('id')
        expert = ExpertProfile.objects.filter(user_id=user_id).first()

        if not expert:
            return GraphQLError(EXPERT_NOT_FOUND_MESSAGE)

        return expert

    def resolve_entrepreneur_profile(self, info, **kwargs):
        user_id = kwargs.get('id')
        entrepreneur = EntrepreneurProfile.objects.filter(user_id=user_id).first()

        if not entrepreneur:
            return GraphQLError(ENTREPRENEUR_NOT_FOUND_MESSAGE)

        return entrepreneur
