# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_override import ProgramOverride
from impact.models.startup import Startup
from impact.models.utils import is_managed


class StartupOverrideGrant(MCModel):
    startup = models.ForeignKey(Startup)
    program_override = models.ForeignKey(ProgramOverride)

    class Meta(MCModel.Meta):
        db_table = 'mc_startupoverridegrant'
        managed = is_managed(db_table)
        verbose_name_plural = 'Startup Override Grants'

    def __str__(self):
        return ("Override grant (%s) for %s for %s" %
                (self.program_override.name,
                 self.startup.name,
                 self.program_override.program.name))
