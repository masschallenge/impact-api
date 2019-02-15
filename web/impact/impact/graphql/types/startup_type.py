import graphene
from graphene_django import DjangoObjectType

from accelerator.models import (
    Startup,
    StartupStatus,
)
from impact.graphql.types import (
    ProgramType
)


class StartupType(DjangoObjectType):
    name = graphene.String()
    high_resolution_logo = graphene.String()
    program = graphene.List(ProgramType)

    class Meta:
        model = Startup
        only_fields = (
            'id',
            'short_pitch',
        )

    def resolve_name(self, info, **kwargs):
        return self.name

    def resolve_high_resolution_logo(self, info, **kwargs):
        if self.high_resolution_logo:
            return self.high_resolution_logo.url

        return None

    def resolve_program(self, info, **kwargs):

        status = StartupStatus.objects.filter(
            startup=self,
            program_startup_status__startup_list_tab_id='finalists'
        ).order_by('-created_at').first()

        if status:
            return [status.program_startup_status.program]

        return []
