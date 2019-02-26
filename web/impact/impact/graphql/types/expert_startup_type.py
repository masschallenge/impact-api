import graphene

from accelerator.models import (
    Startup,
    StartupMentorRelationship,
)
from impact.graphql.types import (
    StartupType,
    ProgramType,
)


class ExpertStartupType(StartupType):
    program = graphene.Field(ProgramType)

    class Meta:
        model = Startup
        only_fields = (
            'id',
            'short_pitch',
        )

    def resolve_program(self, info, **kwargs):
        smr_id = info.variable_values["startup_mentor_relationship_id"]
        smr = StartupMentorRelationship.objects.filter(id=smr_id).first()
        return smr and smr.startup_mentor_tracking.program
