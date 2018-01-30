# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.application_type import ApplicationType
from impact.models.program_cycle import ProgramCycle
from impact.models.startup import Startup
from impact.models.utils import is_managed

import logging

logger = logging.getLogger(__file__)

ERROR_PAYMENT_STATUS = "error"
PAID_PAYMENT_STATUS = "paid"
UNPAID_PAYMENT_STATUS = "unpaid"
PAYMENT_STATUSES = ((PAID_PAYMENT_STATUS, "Paid"),
                    (UNPAID_PAYMENT_STATUS, "Unpaid"),
                    (ERROR_PAYMENT_STATUS, "Payment Error"))


COMPLETE_APP_STATUS = "complete"
INCOMPLETE_APP_STATUS = "incomplete"
SUBMITTED_APP_STATUS = "submitted"
APPLICATION_STATUSES = ((INCOMPLETE_APP_STATUS, "Incomplete"),
                        (COMPLETE_APP_STATUS, "Complete"),
                        (SUBMITTED_APP_STATUS, "Submitted"))


DELAYED_STATUS = "delayed"
FAILED_STATUS = "failed"
INSTANT_STATUS = "instant"
NOT_ELIGIBLE_STATUS = "not_eligible"
REQUIRED_STATUS = "required"
REFUND_STATUSES = ((NOT_ELIGIBLE_STATUS, "Not Eligible For Refund"),
                   (REQUIRED_STATUS, "Refund Due"),
                   (INSTANT_STATUS, "Refund Issued"),
                   (DELAYED_STATUS, "Refund Pending"),
                   (FAILED_STATUS, "Refund Failed"))


class Application(MCModel):
    cycle = models.ForeignKey(ProgramCycle,
                              blank=True,
                              null=True,
                              related_name='applications')
    startup = models.ForeignKey(Startup)
    application_type = models.ForeignKey(ApplicationType)
    application_status = models.CharField(
        blank=True,
        null=True,
        max_length=64,
        choices=APPLICATION_STATUSES,
    )
    submission_datetime = models.DateTimeField(blank=True, null=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_application'
        managed = is_managed(db_table)
        verbose_name_plural = 'Applications'
        ordering = ['startup']

    def __str__(self):
        return '%s for %s by %s' % (self.application_type.name,
                                    self.cycle.name,
                                    self.startup.name)
