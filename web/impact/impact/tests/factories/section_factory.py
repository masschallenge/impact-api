# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import (
    INCLUDE_FOR_CHOICES,
    Section,
)

from .newsletter_factory import NewsletterFactory


class SectionFactory(DjangoModelFactory):

    class Meta:
        model = Section

    heading = Sequence(lambda n: "Heading text {0}".format(n))
    body = Sequence(lambda n: "Newsletter Body {0}".format(n))
    include_for = INCLUDE_FOR_CHOICES[0][0]
    newsletter = SubFactory(NewsletterFactory)
    sequence = Sequence(lambda x: x)
