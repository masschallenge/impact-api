# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.startup import Startup
from impact.models.program_startup_status import ProgramStartupStatus
from impact.models.utils import is_managed


class StartupStatus(MCModel):
    startup = models.ForeignKey(Startup)
    program_startup_status = models.ForeignKey(ProgramStartupStatus)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_startupstatus'
        managed = is_managed(db_table)
        verbose_name_plural = 'Startup Statuses'
        unique_together = ('startup', 'program_startup_status')

    def __str__(self):
        return "Startup Status (%s) for %s" % (
            self.program_startup_status.startup_status, self.startup.name)
