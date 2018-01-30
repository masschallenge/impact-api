# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.partner import Partner
from impact.models.program import Program
from impact.models.utils import is_managed


class RefundCode(MCModel):
    unique_code = models.CharField(max_length=30, unique=True)
    programs = models.ManyToManyField(
        Program,
        help_text=("Which programs is this refund code valid for? "
                   "If no programs are given, then this code can be "
                   "applied to any program."),
        related_name="refund_codes",
        blank=True
    )
    issued_to = models.ForeignKey(Partner, blank=True, null=True)
    discount = models.IntegerField(default=0)
    maximum_uses = models.PositiveIntegerField(
        verbose_name="Maximum Uses",
        help_text=("Indicate the maxiumum number of valid redemptions for "
                   "this code. A null value is interpreted as unlimited."),
        default=1,
        blank=True,
        null=True,
    )
    notes = models.CharField(max_length=300, blank=True)
    internal = models.BooleanField(
        default=False,
        help_text=("If set then this code is intended for internal use "
                   "(e.g, Early Bird discount) and cannot be entered "
                   "directly by users."))

    class Meta(MCModel.Meta):
        db_table = 'accelerator_refundcode'
        managed = is_managed(db_table)
        verbose_name_plural = 'Refund Codes'
