# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.scenario import Scenario
from impact.models.utils import is_managed


class ScenarioJudge(MCModel):
    judge = models.ForeignKey(settings.AUTH_USER_MODEL)
    scenario = models.ForeignKey(Scenario)

    @property
    def stage(self):
        return self.scenario.stage

    class Meta(MCModel.Meta):
        db_table = 'mc_scenariojudge'
        managed = is_managed(db_table)
        verbose_name_plural = 'Scenario Judges'
        unique_together = ('scenario', 'judge')

    def __str__(self):
        return "%s in %s" % (self.judge, self.scenario)
