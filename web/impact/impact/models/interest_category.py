# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.utils import is_managed


class InterestCategory(MCModel):
    name = models.CharField(max_length=127)
    description = models.CharField(max_length=500, blank=True)
    program = models.ForeignKey(Program)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_interestcategory'
        managed = is_managed(db_table)
        verbose_name_plural = "Interest Categories"

    def __str__(self):
        return self.name
