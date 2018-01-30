# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


import decimal
from django.db import models
from django.core.exceptions import ValidationError
from impact.models.application import (
    Application,
    REFUND_STATUSES,
)
from impact.models.mc_model import MCModel
from impact.models.program_cycle import ProgramCycle
from impact.models.refund_code import RefundCode
from impact.models.startup import Startup
from impact.models.utils import is_managed


class RefundCodeRedemption(MCModel):
    refund_code = models.ForeignKey(RefundCode, related_name="redemptions")

    # redeemed_by is no longer used, but is kept for historical purposes
    redeemed_by = models.ForeignKey(
        Application,
        related_name="refund_redemptions",
        blank=True,
        null=True)
    cycle = models.ForeignKey(ProgramCycle)
    startup = models.ForeignKey(Startup, blank=True, null=True)

    refund_status = models.CharField(
        max_length=32,
        choices=REFUND_STATUSES,
        blank=True,
    )
    refund_transaction_id = models.CharField(max_length=500, blank=True)

    # refund_amount is deprecated and should be removed
    refund_amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=decimal.Decimal('0.00'),
    )

    class Meta(MCModel.Meta):
        db_table = 'accelerator_refundcoderedemption'
        managed = is_managed(db_table)

    def __str__(self):
        return "%s redeemed by %s" % (self.refund_code.unique_code,
                                      self.redeemed_by)

    def clean(self):
        num_used_so_far = self.refund_code.redemptions.count()
        max_uses = self.refund_code.maximum_uses
        if (max_uses is not None) and (num_used_so_far >= max_uses):
            msg = "The maximum number of uses for this code has been reached. "
            msg += "Please try another refund code."
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(RefundCodeRedemption, self).save(*args, **kwargs)
