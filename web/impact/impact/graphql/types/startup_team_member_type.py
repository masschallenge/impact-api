import graphene
from graphene_django import DjangoObjectType

from accelerator.models import StartupTeamMember, Startup, EntrepreneurProfile

from impact.graphql.types import (
    StartupType,
)
from impact.graphql.types.entrepreneur_profile_type import (
    EntrepreneurProfileType
)


class StartupTeamMemberType(DjangoObjectType):
    startups = graphene.List(StartupType)
    profile = graphene.Field(EntrepreneurProfileType)

    class Meta:
        model = StartupTeamMember
        only_fields = (
            'title',
            'user',
        )

    def resolve_startups(self, info, **kwargs):
        ids = _startup_team_members({"user": self.user}).values_list(
            'startup', flat=True).distinct()
        startups = Startup.objects.filter(id__in=ids)
        return startups

    def resolve_profile(self, info, **kwargs):
        return EntrepreneurProfile.objects.filter(user=self.user).first()


def _startup_team_members(filters):
    return StartupTeamMember.objects.filter(**filters)
