# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.application_type import ApplicationType
from impact.models.utils import is_managed


class ProgramCycle(MCModel):

    """Association of relatively simultaneous programs"""
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    applications_open = models.BooleanField(default=False)
    application_open_date = models.DateTimeField(blank=True, null=True)
    application_early_deadline_date = models.DateTimeField(
        blank=True,
        null=True)
    application_final_deadline_date = models.DateTimeField(
        blank=True,
        null=True)
    advertised_final_deadline = models.DateTimeField(
        blank=True,
        null=True)
    accepting_references = models.BooleanField(default=False)
    default_application_type = models.ForeignKey(
        ApplicationType,
        null=True,
        blank=True,
        related_name="application_type_for")
    default_overview_application_type = models.ForeignKey(
        ApplicationType,
        null=True,
        blank=True,
        related_name="default_overview_application_type_for")
    hidden = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_programcycle'
        managed = is_managed(db_table)
        verbose_name_plural = "program cycles"

    def __str__(self):
        return self.name
