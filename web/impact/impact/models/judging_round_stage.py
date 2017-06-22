# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.judging_round import JudgingRound
from impact.models.utils import is_managed

import logging
logger = logging.getLogger(__file__)


class JudgingRoundStage(MCModel):
    judging_round = models.ForeignKey(JudgingRound)
    name = models.CharField(max_length=30)  # unique per judging round
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_judgingroundstage'
        managed = is_managed(db_table)
        unique_together = ('judging_round', 'name')

    def __str__(self):
        return "%s of %s" % (self.name, self.judging_round)
