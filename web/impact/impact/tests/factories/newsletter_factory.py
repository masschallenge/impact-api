# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import Newsletter

from .program_factory import ProgramFactory


class NewsletterFactory(DjangoModelFactory):

    class Meta:
        model = Newsletter

    name = Sequence(lambda n: "Newsletter {0}".format(n))
    subject = Sequence(lambda n: "NewsletterSubject {0}".format(n))
    from_addr = Sequence(lambda n: "mcstaffer{0}@mc.org".format(n))
    program = SubFactory(ProgramFactory)
    cc_addrs = ""
    date_mailed = None
