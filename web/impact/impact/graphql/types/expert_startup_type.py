from mc.models import Startup
from .startup_type import StartupType


class ExpertStartupType(StartupType):

    class Meta:
        model = Startup
        only_fields = (
            'id',
            'short_pitch',
        )
