import graphene
from graphql import GraphQLError

from accelerator.models import (
    EntrepreneurProfile,
    ExpertProfile
)
from .types import (
    EntrepreneurProfileType,
    ExpertProfileType
)
from ..permissions.graphql_permissions import can_view_entrepreneur_profile


ENTREPRENEUR_NOT_FOUND_MESSAGE = 'Entrepreneur matching the id does not exist.'
EXPERT_NOT_FOUND_MESSAGE = 'Expert matching the id does not exist.'
NOT_ALLOWED_ACCESS_MESSAGE = 'Sorry, You are not allowed to access this page.'


class Query(graphene.ObjectType):
    expert_profile = graphene.Field(ExpertProfileType, id=graphene.Int())
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
        entrepreneur = EntrepreneurProfile.objects.filter(
            user_id=user_id).first()

        if not entrepreneur:
            return GraphQLError(ENTREPRENEUR_NOT_FOUND_MESSAGE)

        if not can_view_entrepreneur_profile(info.context.user,
                                             entrepreneur.user):
            return GraphQLError(NOT_ALLOWED_ACCESS_MESSAGE)

        return entrepreneur
