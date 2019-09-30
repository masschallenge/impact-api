from accelerator.models import (
    Startup,
)
from impact.graphql.types import (
    StartupType,
)


class ExpertStartupType(StartupType):

    class Meta:
        model = Startup
        only_fields = (
            'id',
            'short_pitch',
        )
