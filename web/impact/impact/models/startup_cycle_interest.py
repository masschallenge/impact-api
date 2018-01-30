# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db.models import (
    ForeignKey,
    ManyToManyField,
)
from impact.models.mc_model import MCModel
from impact.models.startup_program_interest import StartupProgramInterest
from impact.models.program_cycle import ProgramCycle
from impact.models.startup import Startup
from impact.models.utils import is_managed


class StartupCycleInterest(MCModel):
    cycle = ForeignKey(ProgramCycle)
    startup = ForeignKey(Startup)
    interested_programs = ManyToManyField(
        'Program',
        through=StartupProgramInterest)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_startupcycleinterest'
        managed = is_managed(db_table)
