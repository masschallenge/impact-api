# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from simpleuser.models import User

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class ExpertInterest(MCModel):
    user = models.ForeignKey(
        User,
        related_name="expert_interests",
    )
    program_family = models.ForeignKey(
        'ProgramFamily',
        related_name="interested_experts"
    )
    interest_type = models.ForeignKey(
        'ExpertInterestType',
        related_name="interested_experts"
    )
    topics = models.TextField(
        blank=True,
        help_text="Please provide a list of topics of interest to yo"
    )

    class Meta(MCModel.Meta):
        db_table = 'mc_expertinterest'
        managed = is_managed(db_table)
        verbose_name_plural = "Expert Interests"

    def __str__(self):
        msg = "{} interest by {} in the {} program family"
        return msg.format(
            self.interest_type,
            self.user,
            self.program_family
        )
