# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.user_role import UserRole
from impact.models.user_label import UserLabel
from impact.models.utils import is_managed


class ProgramRole(MCModel):
    program = models.ForeignKey(Program)
    name = models.CharField(max_length=30, unique=True, db_index=True)
    user_role = models.ForeignKey(UserRole, null=True, blank=True)
    landing_page = models.CharField(max_length=255, null=True, blank=True)
    newsletter_recipient = models.BooleanField(default=False)

    # March 10, 2016: This is a temporary mechanism to keep old
    # school ProgramRoleGrants in synch with shiny new UserLabels.
    # Going from ProgramRole to UserLabel is good.
    # Going from UserLabel to ProgramRole is bad.
    user_label = models.ForeignKey(UserLabel,
                                   blank=True,
                                   null=True,
                                   related_name="dont_use_commit_fail")

    class Meta(MCModel.Meta):
        db_table = 'mc_programrole'
        managed = is_managed(db_table)
        ordering = ['name', ]
        verbose_name = "Program Role"
        verbose_name_plural = "Program Roles"

    def label_user(self, person):
        if self.user_label:
            self.user_label.users.add(person)

    def __str__(self):
        return self.name
