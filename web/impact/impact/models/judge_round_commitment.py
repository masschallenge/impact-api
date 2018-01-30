# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.judging_round import JudgingRound
from impact.models.utils import is_managed

import logging
logger = logging.getLogger(__file__)


class JudgeRoundCommitment(MCModel):
    judge = models.ForeignKey(settings.AUTH_USER_MODEL)
    judging_round = models.ForeignKey(JudgingRound)
    commitment_state = models.BooleanField(default=True)
    capacity = models.IntegerField(blank=True, null=True)
    current_quota = models.IntegerField(blank=True, null=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_judgeroundcommitment'
        managed = is_managed(db_table)
        verbose_name_plural = ("Judge commitment to participate in a "
                               "Judging Round")
        unique_together = ('judge', 'judging_round')

    def __str__(self):
        return "%s commited to %s" % (self.judge, self.judging_round)
