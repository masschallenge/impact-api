# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.interest_category import InterestCategory
from impact.models.newsletter import Newsletter
from impact.models.utils import is_managed

ANY_SPECIFIED_CATEGORY = 'ANY_SPECIFIED_CATEGORY'

INCLUDE_FOR_CHOICES = (('EVERYONE', 'Everyone'),
                       (ANY_SPECIFIED_CATEGORY, 'Any specified category'))

SECTION_SEQUENCE_HELP = "specify the order of this section in the newsletter"


class Section(MCModel):
    heading = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    interest_categories = models.ManyToManyField(
        InterestCategory,
        blank=True)
    include_for = models.CharField(
        max_length=32,
        choices=INCLUDE_FOR_CHOICES,
        default='EVERYONE')
    newsletter = models.ForeignKey(Newsletter, related_name='sections')
    sequence = models.PositiveIntegerField(help_text=SECTION_SEQUENCE_HELP)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_section'
        managed = is_managed(db_table)
        ordering = ('newsletter', 'sequence', )

    def __str__(self):
        return self.heading
