# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models import Program
from impact.models.utils import is_managed


PROGRAM_ADMINISTRATOR_PERMISSIONS = [
    ('view', 'Can view'),
    ('export', 'Can export'),
    ('change', 'Can change'),
    ('add', 'Can add'),
    ('delete', 'Can delete'),
]


class ProgramAdministratorPermission(MCModel):
    program = models.ForeignKey(Program)
    model = models.CharField(
        choices=[],
        max_length=64,
    )
    permission = models.CharField(
        choices=PROGRAM_ADMINISTRATOR_PERMISSIONS,
        max_length=20,
    )
    description = models.CharField(max_length=200, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_programadministratorpermission'
        managed = is_managed(db_table)
        verbose_name_plural = 'Program Administrator Permissions'

    def __str__(self):
        return "%s %s: %s" % (self.program.name,
                              self.model,
                              self.permission)
