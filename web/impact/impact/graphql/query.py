import graphene

from impact.graphql.types import (
    EntrepreneurProfileType,
    ExpertProfileType,
)
from accelerator.models import (
    EntrepreneurProfile,
    ExpertProfile,
    UserRole,
)
from accelerator_abstract.models.base_user_utils import is_employee
from graphql import GraphQLError

ENTREPRENEUR_NOT_FOUND_MESSAGE = 'Entrepreneur matching the id does not exist.'
EXPERT_NOT_FOUND_MESSAGE = 'Expert matching the id does not exist.'
NOT_ALLOWED_ACCESS_MESSAGE = 'Sorry, You are not allowed to access this page.'


def visible_roles(current_user):
    basic_user_roles = [
        UserRole.FINALIST,
        UserRole.AIR,
        UserRole.MENTOR,
        UserRole.PARTNER,
        UserRole.ALUM
    ]
    basic_visible_roles = [UserRole.FINALIST, UserRole.STAFF, UserRole.ALUM]

    current_user_roles = list(
        current_user.programrolegrant_set.values_list(
            'program_role__user_role__name', flat=True).distinct()
    )
    if not current_user_roles:
        return [UserRole.STAFF]
    if set(basic_user_roles).intersection(current_user_roles):
        return basic_visible_roles + [UserRole.MENTOR]
    if UserRole.JUDGE in current_user_roles:
        return basic_visible_roles


def has_permission(profile_user, roles):
    return profile_user.programrolegrant_set.filter(
        program_role__user_role__name__in=roles).exists()


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

        if not is_employee(info.context.user):
            roles = visible_roles(info.context.user)
            if not has_permission(entrepreneur.user, roles):
                return GraphQLError(NOT_ALLOWED_ACCESS_MESSAGE)

        return entrepreneur
