import graphene
from graphene_django import DjangoObjectType

from accelerator.models import (
    Startup,
)
from impact.graphql.types import (
    ProgramType
)


class StartupType(DjangoObjectType):
    name = graphene.String()
    high_resolution_logo = graphene.String()
    program = graphene.Field(ProgramType)

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
