# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
try:
    from sorl.thumbnail import ImageField
    HAS_SORL = True
except ImportError:
    HAS_SORL = False

from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.utils import is_managed


PARTNER_BADGE_DISPLAY_VALUES = (
    ('NONE', 'None'),
    ('PARTNER_LIST', 'Only on partner list'),
    ('PARTNER_PROFILE', 'Only on partner profile'),
    ('PARTNER_LIST_AND_PROFILE', 'Partner list and profile'))


class ProgramPartnerType(MCModel):
    program = models.ForeignKey(Program)
    partner_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    feature_in_footer = models.BooleanField(default=False)
    sort_order = models.IntegerField(
        blank=True,
        null=True)
    if HAS_SORL:
        badge_image = ImageField(
            upload_to='badge_images',
            blank=True)
    else:
        badge_image = models.CharField(max_length=100, null=True)

    badge_display = models.CharField(choices=PARTNER_BADGE_DISPLAY_VALUES,
                                     max_length=30, default="NONE")

    class Meta(MCModel.Meta):
        db_table = 'accelerator_programpartnertype'
        managed = is_managed(db_table)
        verbose_name_plural = 'Program Partner Types'
        ordering = ['program', 'sort_order', ]

    def __str__(self):
        return "Partner type %s for %s" % (self.partner_type,
                                           self.program.name)
