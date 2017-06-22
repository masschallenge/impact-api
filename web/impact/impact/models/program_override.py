# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


import decimal

from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_cycle import ProgramCycle
from impact.models.utils import is_managed


class ProgramOverride(MCModel):
    cycle = models.ForeignKey(ProgramCycle,
                              blank=True,
                              null=True,
                              related_name='program_overrides')
    program = models.ForeignKey("Program")
    # this field will be removed after data migration
    name = models.CharField(max_length=50)
    applications_open = models.BooleanField(default=False)
    application_open_date = models.DateTimeField(blank=True, null=True)
    application_early_deadline_date = models.DateTimeField(blank=True,
                                                           null=True)
    application_final_deadline_date = models.DateTimeField(blank=True,
                                                           null=True)
    early_application_fee = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=decimal.Decimal('0.00'),
    )
    regular_application_fee = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=decimal.Decimal('0.00'),
    )

    class Meta(MCModel.Meta):
        db_table = 'mc_programoverride'
        managed = is_managed(db_table)
        verbose_name_plural = 'Program Overrides'

    def __str__(self):
        return "Program override (%s) for %s" % (self.name, self.program.name)
