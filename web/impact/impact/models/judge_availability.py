# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.judge_round_commitment import JudgeRoundCommitment
from impact.models.panel_time import PanelTime
from impact.models.panel_type import PanelType
from impact.models.panel_location import PanelLocation
from impact.models.utils import is_managed


class JudgeAvailability(MCModel):
    commitment = models.ForeignKey(JudgeRoundCommitment)
    panel_location = models.ForeignKey(PanelLocation, blank=True, null=True)
    panel_time = models.ForeignKey(PanelTime, blank=True, null=True)
    panel_type = models.ForeignKey(PanelType, blank=True, null=True)
    availability_type = models.CharField(
        max_length=32,
        choices=(("Preferred", "Preferred"), ("Available", "Available"),
                 ("Not Available", "Not Available"))
    )

    class Meta(MCModel.Meta):
        db_table = 'accelerator_judgeavailability'
        managed = is_managed(db_table)
        verbose_name_plural = ("Judge availability for specific Panel types, "
                               "times, locations")
        unique_together = ('commitment', 'panel_location', 'panel_time',
                           'panel_type')
        ordering = ['panel_time__start_date_time', 'panel_type__panel_type',
                    'panel_location__location']
