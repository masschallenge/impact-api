# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Iterator,
    SubFactory,
)

from impact.models import (
    INSTANT_STATUS,
    RefundCodeRedemption,
)

from .refund_code_factory import RefundCodeFactory
from .startup_factory import StartupFactory
from .program_cycle_factory import ProgramCycleFactory


class RefundCodeRedemptionFactory(DjangoModelFactory):

    class Meta:
        model = RefundCodeRedemption

    refund_code = SubFactory(RefundCodeFactory)
    redeemed_by = None
    startup = SubFactory(StartupFactory)
    refund_status = INSTANT_STATUS
    refund_transaction_id = ""
    refund_amount = Iterator([10, 25, 50, 100])
    cycle = SubFactory(ProgramCycleFactory)
