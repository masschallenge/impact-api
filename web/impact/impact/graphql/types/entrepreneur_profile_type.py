import graphene
from accelerator.models import (
    EntrepreneurProfile,
    Startup,
    StartupTeamMember
)
from impact.graphql.types import BaseUserProfileType
from .entrepreneur_startup_type import EntrepreneurStartupType


class EntrepreneurProfileType(BaseUserProfileType):
    image_url = graphene.String()
    title = graphene.String()
    startups = graphene.List(EntrepreneurStartupType)

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
