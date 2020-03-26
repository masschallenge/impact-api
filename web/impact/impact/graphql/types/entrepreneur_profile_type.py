import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from accelerator.models import (
    EntrepreneurProfile,
    UserRole,
    Startup,
    StartupRole,
    StartupTeamMember
)

from impact.graphql.types.entrepreneur_startup_type import (
    EntrepreneurStartupType,
)

from impact.utils import get_user_program_and_startup_roles

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


    def resolve_program_roles(self, info, **kwargs):
        user_roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        startup_roles_of_interest = [StartupRole.ENTRANT]
        return get_user_program_and_startup_roles(
            self.user, user_roles_of_interest, startup_roles_of_interest)
