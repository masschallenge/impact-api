# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import PayPalPayment

from .program_cycle_factory import ProgramCycleFactory
from .startup_factory import StartupFactory


class PayPalPaymentFactory(DjangoModelFactory):

    class Meta:
        model = PayPalPayment

    startup = SubFactory(StartupFactory)
    cycle = SubFactory(ProgramCycleFactory)
    token = Sequence(lambda n: "PayPal Token {0}".format(n))
    transaction = Sequence(lambda n: "PayPal Transaction {0}".format(n))
    amount = 99.0
    currency_code = "USD"
    refundable = True
