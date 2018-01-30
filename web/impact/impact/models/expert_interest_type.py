# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class ExpertInterestType(MCModel):
    """A category of involvement an expert has with a program or program family
    """
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=255)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_expertinteresttype'
        managed = is_managed(db_table)
        verbose_name_plural = "Expert Interest Types"

    def __str__(self):
        return self.name
