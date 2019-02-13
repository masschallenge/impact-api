import graphene
from graphene_django import DjangoObjectType

from accelerator.models import (
    Startup,
    Program,
    Application,
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
        cycles = Application.objects.filter(
            startup=self).values_list("cycle", flat=True)
        return [
            program
            for program in Program.objects.filter(cycle_id__in=cycles)]
