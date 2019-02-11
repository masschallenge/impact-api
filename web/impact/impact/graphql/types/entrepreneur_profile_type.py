import graphene
from graphene_django import DjangoObjectType
from accelerator.models import (
    EntrepreneurProfile,
    StartupTeamMember,
    Startup,
)
from impact.graphql.types import (
    StartupType
)


class EntrepreneurProfileType(DjangoObjectType):
    startups = graphene.List(StartupType)
    image_url = graphene.String()
    title = graphene.String()
    current_program = graphene.String()

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
        ids = _startup_team_members(self.user).values_list(
            'startup', flat=True).distinct()
        startups = Startup.objects.filter(id__in=ids)
        return [startup for startup in startups]

    def resolve_title(self, info, **kwargs):
        return _startup_team_members(self.user).values_list(
            'title', flat=True).distinct()[0]

    def resolve_current_program(self, info, **kwargs):
        return self.current_program.name


def _startup_team_members(user):
    return StartupTeamMember.objects.filter(user=user)
