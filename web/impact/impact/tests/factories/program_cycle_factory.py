# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import ProgramCycle
from impact.tests.utils import months_from_now

from .application_type_factory import ApplicationTypeFactory


class ProgramCycleFactory(DjangoModelFactory):

    class Meta:
        model = ProgramCycle

    name = Sequence(lambda n: "Program Cycle {0}".format(n))
    applications_open = False
    application_open_date = months_from_now(-5)
    application_early_deadline_date = months_from_now(-4)
    application_final_deadline_date = months_from_now(-3)
    advertised_final_deadline = months_from_now(-3)
    accepting_references = False
    default_application_type = SubFactory(ApplicationTypeFactory)
    default_overview_application_type = SubFactory(
        ApplicationTypeFactory)
    hidden = False
