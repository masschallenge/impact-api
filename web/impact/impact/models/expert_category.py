# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class ExpertCategory(MCModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_expertcategory'
        managed = is_managed(db_table)
        ordering = ['name', ]
        verbose_name = "Expert Category"
        verbose_name_plural = "Expert Categories"

    def __str__(self):
        return self.name
