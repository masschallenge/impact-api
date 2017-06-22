# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class PanelTime(MCModel):
    day = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    start_date_time = models.DateTimeField(blank=False, null=True)
    end_date_time = models.DateTimeField(blank=False, null=True)
    judging_round = models.ForeignKey("JudgingRound", blank=True, null=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_paneltime'
        managed = is_managed(db_table)
        verbose_name_plural = "Panel Times"

    def __str__(self):
        return self.create_time_frame(self.start_date_time)
