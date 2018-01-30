# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import (
    LABEL_LENGTH,
    is_managed,
)


class NamedGroup(MCModel):
    name = models.CharField(max_length=LABEL_LENGTH, default="")

    class Meta(MCModel.Meta):
        db_table = 'accelerator_namedgroup'
        managed = is_managed(db_table)
        ordering = ["name"]

    def __str__(self):
        return self.name
