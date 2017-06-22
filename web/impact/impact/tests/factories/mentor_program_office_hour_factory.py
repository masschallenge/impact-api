# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import (
    date,
    timedelta,
)
from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import (
    MC_BOS_LOCATION,
    MentorProgramOfficeHour,
)

from .entrepreneur_factory import EntrepreneurFactory
from .expert_factory import ExpertFactory
from .program_factory import ProgramFactory


class MentorProgramOfficeHourFactory(DjangoModelFactory):

    class Meta:
        model = MentorProgramOfficeHour

    program = SubFactory(ProgramFactory)
    mentor = SubFactory(ExpertFactory)
    finalist = SubFactory(EntrepreneurFactory)
    date = date.today() + timedelta(days=3)
    start_time = '10:00'
    end_time = '12:00'
    location = MC_BOS_LOCATION
    description = Sequence(lambda n: "Description office hour {0}".format(n))
    notify_reservation = True
    topics = Sequence(lambda n: "Topics for test office hour {0}".format(n))
