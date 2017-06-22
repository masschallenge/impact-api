# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from simpleuser.models import User
from impact.models.mc_model import MCModel
from impact.models.program_role import ProgramRole
from impact.models.utils import is_managed


class ProgramRoleGrant(MCModel):
    person = models.ForeignKey(User)
    program_role = models.ForeignKey(ProgramRole)

    class Meta(MCModel.Meta):
        db_table = 'mc_programrolegrant'
        managed = is_managed(db_table)
        unique_together = ('person', 'program_role')
        verbose_name = "Program Role Grant"
        verbose_name_plural = "Program Role Grants"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.program_role.label_user(self.person)
        super(ProgramRoleGrant, self).save(*args, **kwargs)

    def __str__(self):
        return "Role %s for %s" % (self.program_role, self.person)
