# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import (
    datetime,
    timedelta,
)
from pytz import utc

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import (
    Application,
    INCOMPLETE_APP_STATUS,
)

from .application_type_factory import ApplicationTypeFactory
from .program_cycle_factory import ProgramCycleFactory
from .startup_factory import StartupFactory


class ApplicationFactory(DjangoModelFactory):

    class Meta:
        model = Application

    cycle = SubFactory(ProgramCycleFactory)
    startup = SubFactory(StartupFactory)
    application_type = SubFactory(ApplicationTypeFactory)
    application_status = INCOMPLETE_APP_STATUS
    submission_datetime = utc.localize(datetime.now() + timedelta(-2))
