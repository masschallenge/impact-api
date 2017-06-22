# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


import decimal

from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_cycle import ProgramCycle
from impact.models.startup import Startup
from impact.models.utils import is_managed


# Conforming to the django-paypal convention of using
# PayPal in CamelCase and paypal in snake_case.
class PayPalPayment(MCModel):
    startup = models.ForeignKey(Startup)
    cycle = models.ForeignKey(ProgramCycle)
    token = models.CharField(max_length=100)
    transaction = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=7,
                                 decimal_places=2,
                                 default=decimal.Decimal("0.00"))
    currency_code = models.CharField(max_length=3, default='')
    refundable = models.BooleanField(default=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_paypalpayment'
        managed = is_managed(db_table)
