# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import (
    LABEL_LENGTH,
    is_managed,
)


class UserLabel(MCModel):
    label = models.CharField(max_length=LABEL_LENGTH)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_userlabel'
        managed = is_managed(db_table)
        ordering = ["label", ]

    def __str__(self):
        return self.label

    def add_program_role(self, program_role):
        self.users.add(*[prg.person
                         for prg in program_role.programrolegrant_set.all()])

    def add(self, user):
        self.users.add(user)
