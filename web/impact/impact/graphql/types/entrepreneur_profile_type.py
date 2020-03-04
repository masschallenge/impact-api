import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from accelerator.models import (
    EntrepreneurProfile,
    UserRole,
    Startup,
    StartupTeamMember
)

from impact.graphql.types.entrepreneur_startup_type import (
    EntrepreneurStartupType,
)

from impact.utils import (
    get_user_startup_prg_role_by_program_family, combine_prg_roles,
    get_user_prg_role_by_program_family
)

class EntrepreneurProfileType(DjangoObjectType):
    image_url = graphene.String()
    title = graphene.String()
    startups = graphene.List(EntrepreneurStartupType)
    program_roles = GenericScalar()

    class Meta:
        model = EntrepreneurProfile
        only_fields = (
            'facebook_url',
            'linked_in_url',
            'personal_website_url',
            'phone',
            'twitter_handle',
            'user',
        )

    def resolve_image_url(self, info, **kwargs):
        return self.image and self.image.url

    def resolve_startups(self, info, **kwargs):
        ids = StartupTeamMember.objects.filter(user=self.user).values_list(
            'startup', flat=True).distinct()
        return Startup.objects.filter(id__in=ids)

    def resolve_title(self, info, **kwargs):
        team_member = self.user.startupteammember_set.last()
        if team_member:
            return team_member.title
        return ""

    """
    fetch a program role assigned to an user and those assigned to the startups
    the user belong to

    Time, Space, Query Complexity
    Query: amount to the query complexity of the two helper function that
    access the DB (see functions for query comp analysis for each)

    Time/Space amount to time and space complexity of the three helper functions
    (see functions for time/space comp analysis for each)
    """
    def resolve_program_roles(self, info, **kwargs):
        roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        user_prg_roles = get_user_prg_role_by_program_family(
            self.user, roles_of_interest)

        startup_prg_roles = get_user_startup_prg_role_by_program_family(
           self.user
        )
        return combine_prg_roles(
            user_prg_roles=user_prg_roles, startup_prg_roles=startup_prg_roles
        )
