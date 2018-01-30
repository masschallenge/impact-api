# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.utils import is_managed
from impact.models.mc_model import MCModel

CLEARANCE_FORMAT_STR = u"Clearance {level} at {program_family} for {user}"

CLEARANCE_LEVEL_EXEC_MD = "Exec/MD"
CLEARANCE_LEVEL_GLOBAL_MANAGER = "Global Manager"
CLEARANCE_LEVEL_POM = "Program Operations Manager"
CLEARANCE_LEVELS = [
    CLEARANCE_LEVEL_EXEC_MD,
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    CLEARANCE_LEVEL_POM
]
CLEARANCE_LEVEL_ORDER = {level: i for i, level in enumerate(CLEARANCE_LEVELS)}
CLEARANCE_LEVEL_CHOICES = [(x, x) for x in CLEARANCE_LEVELS]


class Clearance(MCModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False,
                             blank=False,
                             related_name="clearances")
    level = models.CharField(choices=CLEARANCE_LEVEL_CHOICES,
                             null=False,
                             blank=False,
                             max_length=64)
    program_family = models.ForeignKey("ProgramFamily",
                                       null=False,
                                       blank=False,
                                       related_name="user_clearances")

    # Accelerate Model uses a Custom Manager, currently not implemented here.

    class Meta(MCModel.Meta):
        unique_together = ("user", "program_family")
        db_table = 'accelerator_clearance'
        managed = is_managed(db_table)

    def __str__(self):
        return CLEARANCE_FORMAT_STR.format(level=self.level,
                                           program_family=self.program_family,
                                           user=self.user)
