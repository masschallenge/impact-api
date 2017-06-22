# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


import decimal

from django.db import models

from impact.models.mc_model import MCModel
from impact.models.paypal_payment import PayPalPayment
from impact.models.utils import is_managed


# Conforming to the django-paypal convention of using
# PayPal in CamelCase and paypal in snake_case.
class PayPalRefund(MCModel):
    payment = models.ForeignKey(PayPalPayment)
    status = models.CharField(max_length=100, blank=True)
    transaction = models.CharField(max_length=100, blank=True)
    correlation = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=7,
                                 decimal_places=2,
                                 default=decimal.Decimal("0.00"))

    class Meta(MCModel.Meta):
        db_table = 'mc_paypalrefund'
        managed = is_managed(db_table)
