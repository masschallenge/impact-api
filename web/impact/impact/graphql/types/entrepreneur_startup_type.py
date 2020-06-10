import graphene

from mc.models import (
    StartupStatus,
    Startup,
)
from .startup_type import StartupType
from .program_type import ProgramType


class EntrepreneurStartupType(StartupType):
    program = graphene.Field(ProgramType)

    class Meta:
        model = Startup
        only_fields = (
            'id',
            'short_pitch',
        )

    def resolve_program(self, info, **kwargs):
        status = StartupStatus.objects.filter(
            startup=self,
            program_startup_status__startup_list_tab_id='finalists'
        ).order_by('-created_at').first()
        if status:
            return status.program_startup_status.program
