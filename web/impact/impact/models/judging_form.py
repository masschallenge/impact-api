# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class JudgingForm(MCModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_judgingform'
        managed = is_managed(db_table)
        verbose_name_plural = 'Judging Forms'

    def __str__(self):
        return self.name
