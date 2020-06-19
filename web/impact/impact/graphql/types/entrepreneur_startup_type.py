import graphene

from .startup_type import StartupType
from .program_type import ProgramType
from mc.models import (
    StartupStatus,
    Startup,
)

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(">>>>>>>>>>>>>>>>>>>>>", dir_path)

cwd = os.getcwd()
print(".........................", cwd)



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
