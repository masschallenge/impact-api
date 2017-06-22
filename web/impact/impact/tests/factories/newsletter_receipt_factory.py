# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import NewsletterReceipt

from .entrepreneur_factory import EntrepreneurFactory
from .newsletter_factory import NewsletterFactory


class NewsletterReceiptFactory(DjangoModelFactory):

    class Meta:
        model = NewsletterReceipt

    newsletter = SubFactory(NewsletterFactory)
    recipient = SubFactory(EntrepreneurFactory)
