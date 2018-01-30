# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


import logging
logger = logging.getLogger(__file__)


class NewsletterReceipt(MCModel):
    newsletter = models.ForeignKey("Newsletter")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_newsletterreceipt'
        managed = is_managed(db_table)
        pass

    def __str__(self):
        return "%s sent to %s" % (self.newsletter, self.recipient)
