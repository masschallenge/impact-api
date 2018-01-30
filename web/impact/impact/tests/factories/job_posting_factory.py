# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from pytz import utc
from datetime import (
    datetime,
    timedelta,
)

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import JobPosting

from impact.tests.factories.startup_factory import StartupFactory


class JobPostingFactory(DjangoModelFactory):

    class Meta:
        model = JobPosting

    startup = SubFactory(StartupFactory)
    postdate = utc.localize(datetime.now() - timedelta(1))
    type = Sequence(lambda n: "type {0}".format(n))
    title = Sequence(lambda n: "engineer level {0}".format(n))
    description = "Create mission-critical brand technologies"
    applicationemail = "null@example.com"
    more_info_url = Sequence(lambda n: "http://example.com/job{0}".format(n))
