# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class PanelType(MCModel):
    panel_type = models.CharField(max_length=225, primary_key=True)
    description = models.CharField(max_length=225)
    judging_round = models.ForeignKey("JudgingRound", blank=True, null=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_paneltype'
        managed = is_managed(db_table)
        verbose_name_plural = "Panel Types"

    def __str__(self):
        return self.description
