# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_role import ProgramRole
from impact.models.utils import is_managed


class Observer(MCModel):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="Email address", max_length=100)
    title = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=50, blank=True)
    newsletter_cc_roles = models.ManyToManyField(
        ProgramRole,
        blank=True)
    newsletter_sender = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_observer'
        managed = is_managed(db_table)
        ordering = ['last_name', 'first_name']
        verbose_name = "Observer"
        verbose_name_plural = "Observers"

    def __str__(self):
        if self.first_name:
            full_name = "%s, %s" % (self.last_name, self.first_name)
        else:
            full_name = self.last_name
        return "%s (%s)" % (full_name, self.email)
