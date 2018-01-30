# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.application import Application
from impact.models.judging_round import JudgingRound
from impact.models.utils import is_managed


DEFAULT_PANEL_SIZE = 10


class Scenario(MCModel):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=512, blank=True)
    judges = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="scenarios",
        through="impact.ScenarioJudge")
    applications = models.ManyToManyField(
        Application,
        related_name="scenarios",
        through="impact.ScenarioApplication")
    judging_round = models.ForeignKey(JudgingRound)
    # Default False and set True when selected. Only one may be True.
    is_active = models.BooleanField(default=False)
    panel_size = models.IntegerField(blank=True,
                                     default=DEFAULT_PANEL_SIZE,
                                     null=False)
    max_panels_per_judge = models.IntegerField(blank=True, null=True)
    min_panels_per_judge = models.IntegerField(blank=True,
                                               default=0,
                                               null=False)
    sequence_number = models.PositiveIntegerField(
        help_text="Indicate the order for this scenario within the stage",
        blank=True,
        null=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_scenario'
        managed = is_managed(db_table)
        unique_together = (('name', 'judging_round'),
                           ('judging_round', 'sequence_number'), )

    def __str__(self):
        return self.name
