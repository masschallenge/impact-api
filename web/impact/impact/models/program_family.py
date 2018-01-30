# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class ProgramFamily(MCModel):

    """Association of related programs"""
    name = models.CharField(max_length=128)
    short_description = models.TextField(
        blank=True,
        help_text="You may use HTML, including links",
    )
    url_slug = models.CharField(
        max_length=30,
        default="",
    )
    email_domain = models.CharField(
        max_length=30,
        default="",
        help_text="Base domain for role-based email"
    )
    phone_number = models.CharField(
        max_length=30,
        default="",
        help_text="Phone number for this program (local form)"
    )
    physical_address = models.TextField(
        default="",
    )
    office_hour_bcc = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        help_text="An email address to bcc whenever office hours"
                  " are created, deleted, or modified in this program family"
    )
    is_open = models.BooleanField(
        default=True,
        help_text="Whether this ProgramFamily should be available to"
                  " entrepreneurs and experts"
    )

    class Meta(MCModel.Meta):
        db_table = 'accelerator_programfamily'
        managed = is_managed(db_table)
        verbose_name_plural = "program families"

    def __str__(self):
        return self.name
