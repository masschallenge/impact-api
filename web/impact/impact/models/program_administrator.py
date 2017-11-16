# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_administrator_permission import (
    ProgramAdministratorPermission,
)
from impact.models.utils import is_managed


class ProgramAdministrator(MCModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    permission = models.ManyToManyField(
        ProgramAdministratorPermission,
        related_name="administrator_permissions")

    class Meta(MCModel.Meta):
        db_table = 'mc_programadministrator'
        managed = is_managed(db_table)
        verbose_name_plural = 'Program Administrator'

    def __str__(self):
        return "Program administrator permissions for %s" % self.user
