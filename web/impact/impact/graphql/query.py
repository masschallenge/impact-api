import graphene

from impact.graphql.types import (
    ExpertProfileType,
    StartupTeamMemberType,
)
from accelerator.models import (
    ExpertProfile,
    StartupTeamMember,
)
from graphql import GraphQLError
EXPERT_NOT_FOUND_MESSAGE = 'Expert matching the id does not exist.'
TEAM_MEMBER_NOT_FOUND_MESSAGE = (
    'Startup Team Member matching id does not exist'
)


class Query(graphene.ObjectType):
    expert_profile = graphene.Field(
        ExpertProfileType, id=graphene.Int())
    entrepreneur_profile = graphene.Field(
        StartupTeamMemberType, id=graphene.Int())

    def resolve_expert_profile(self, info, **kwargs):
        user_id = kwargs.get('id')

        if user_id is not None:
            expert = ExpertProfile.objects.filter(user_id=user_id).first()

            if not expert:
                return GraphQLError(EXPERT_NOT_FOUND_MESSAGE)

            return expert

        return GraphQLError("Ensure url specifies an expert id")

    def resolve_entrepreneur_profile(self, info, **kwargs):
        team_member_id = kwargs.get('id')

        if team_member_id is not None:
            team_member = StartupTeamMember.objects.filter(
                id=team_member_id).first()

            if not team_member:
                return GraphQLError(TEAM_MEMBER_NOT_FOUND_MESSAGE)

            return team_member

        return GraphQLError("Ensure url specifies a team member id")
