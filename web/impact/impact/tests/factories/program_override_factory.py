# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
from pytz import utc
from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from accelerator.models import ProgramOverride

from .program_cycle_factory import ProgramCycleFactory
from .program_factory import ProgramFactory


class ProgramOverrideFactory(DjangoModelFactory):
    class Meta:
        model = ProgramOverride

    program = SubFactory(ProgramFactory)
    cycle = SubFactory(ProgramCycleFactory)
    name = Sequence(lambda n: "{0}".format(n))
    applications_open = True
    application_open_date = utc.localize(datetime(2015, 1, 1))
    application_early_deadline_date = utc.localize(datetime(2015, 1, 8))
    application_final_deadline_date = utc.localize(datetime(2015, 1, 15))
    early_application_fee = 50.00
    regular_application_fee = 100
