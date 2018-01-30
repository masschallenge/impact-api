# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.partner import Partner
from impact.models.program import Program
from impact.models.program_partner_type import ProgramPartnerType
from impact.models.utils import is_managed


class ProgramPartner(MCModel):
    program = models.ForeignKey(Program)
    partner = models.ForeignKey(Partner)
    partner_type = models.ForeignKey(ProgramPartnerType)
    description = models.TextField(
        max_length=2000,
        blank=True,
        help_text='This is the description of the Partner '
        'SPECIFICALLY IN THE CONTEXT OF THE PROGRAM. '
        '(Distinct from the generic description of the Partner.) '
        'For example, description of In-Kind sponsorship deals specific '
        'to a Program would go here.')

    class Meta(MCModel.Meta):
        db_table = 'accelerator_programpartner'
        managed = is_managed(db_table)
        verbose_name_plural = 'Program Partner'
        ordering = ['program__name', 'partner_type__sort_order', 'partner', ]

    def __str__(self):
        return "%s Partner %s from %s" % (self.partner_type.partner_type,
                                          self.partner.name,
                                          self.program.name)
