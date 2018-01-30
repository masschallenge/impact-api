# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.program_role import ProgramRole
from impact.models.utils import is_managed
import logging

logger = logging.getLogger(__file__)

FIRST_NAME = 1
LAST_NAME = 2
EMAIL = 0


EMAIL_TEMPLATE = "newsletter/newsletter_email.html"


class Newsletter(MCModel):
    name = models.CharField(max_length=127)
    subject = models.CharField(
        max_length=500,  # long to allow for template code
        blank=True,
        help_text='Best practice: keep subject lines short')
    from_addr = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    recipient_roles = models.ManyToManyField(
        ProgramRole,
        limit_choices_to={
            'newsletter_recipient': True,
        },
        blank=True)
    program = models.ForeignKey(Program)
    cc_addrs = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Zero or more email addresses to CC; separate with commas")
    date_mailed = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_newsletter'
        managed = is_managed(db_table)
        ordering = ('-created_at', 'name', )

    def __str__(self):
        return self.name
