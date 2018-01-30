# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.partner import Partner
from impact.models.utils import is_managed


class PartnerTeamMember(MCModel):
    partner = models.ForeignKey(Partner)
    team_member = models.ForeignKey(settings.AUTH_USER_MODEL)
    partner_administrator = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_partnerteammember'
        managed = is_managed(db_table)
        verbose_name_plural = 'Partner Team Members'
        ordering = ['team_member__first_name']
        unique_together = ('partner', 'team_member')

    def __str__(self):
        return "Member %s from %s" % (self.team_member,
                                      self.partner.name)
