# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.application import Application
from impact.models.scenario import Scenario
from impact.models.utils import is_managed


class ScenarioApplication(MCModel):
    application = models.ForeignKey(Application)
    scenario = models.ForeignKey(Scenario)
    # default 1. How much do we want this application assigned now?
    # Set higher for foreign and early bird.
    priority = models.IntegerField(default=1)

    class Meta(MCModel.Meta):
        db_table = 'mc_scenarioapplication'
        managed = is_managed(db_table)
        verbose_name_plural = 'Scenario Applications'
        unique_together = ('scenario', 'application')

    def __str__(self):
        return "%s in %s" % (self.application, self.scenario)
