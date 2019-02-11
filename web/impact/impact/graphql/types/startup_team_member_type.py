from graphene_django import DjangoObjectType

from accelerator.models import StartupTeamMember


class StartupTeamMemberType(DjangoObjectType):
    class Meta:
        model = StartupTeamMember
        only_fields = (
            'title',
        )
