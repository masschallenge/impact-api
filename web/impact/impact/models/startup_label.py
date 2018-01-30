# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.startup import Startup
from impact.models.utils import LABEL_LENGTH
from impact.models.utils import is_managed


class StartupLabel(MCModel):
    label = models.CharField(max_length=LABEL_LENGTH)
    startups = models.ManyToManyField(Startup, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_startuplabel'
        managed = is_managed(db_table)
        ordering = ["label", ]

    def __str__(self):
        return self.label

    def add_program_startup_status(self, status):
        self.startups.add(*status.startups())
