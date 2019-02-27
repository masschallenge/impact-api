import graphene
from graphene_django import DjangoObjectType

from accelerator.models import StartupTeamMember, Startup, EntrepreneurProfile

from impact.graphql.types.entrepreneur_startup_type import (
    EntrepreneurStartupType,
)
from impact.graphql.types.entrepreneur_profile_type import (
    EntrepreneurProfileType
)


class StartupTeamMemberType(DjangoObjectType):
    startups = graphene.List(EntrepreneurStartupType)
    profile = graphene.Field(EntrepreneurProfileType)

    class Meta:
        model = StartupTeamMember
        only_fields = (
            'title',
            'user',
        )

    def resolve_startups(self, info, **kwargs):
        ids = StartupTeamMember.objects.filter(user=self.user).values_list(
            'startup', flat=True).distinct()
        return Startup.objects.filter(id__in=ids)

    def resolve_profile(self, info, **kwargs):
        return EntrepreneurProfile.objects.filter(user=self.user).first()
