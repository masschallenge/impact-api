import graphene

from impact.graphql.types.expert_profile_type import ExpertProfileType
from impact.graphql.types.entrepreneur_profile_type import (
    EntrepreneurProfileType
)
from accelerator.models import (
    ExpertProfile,
    EntrepreneurProfile,
    StartupTeamMember,
)
from graphql import GraphQLError
EXPERT_NOT_FOUND_MESSAGE = 'Expert matching the id does not exist.'


class Query(graphene.ObjectType):
    expert_profile = graphene.Field(
        ExpertProfileType, id=graphene.Int())
    entrepreneur_profile = graphene.Field(
        EntrepreneurProfileType, id=graphene.Int())

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
            user_id = StartupTeamMember.objects.filter(
                id=team_member_id).values_list("user_id", flat=True)

            if not user_id:
                return GraphQLError("Startup Team Member does not exist")

            return EntrepreneurProfile.objects.filter(user_id=user_id).first()

        return GraphQLError("Ensure url specifies a team member id")
