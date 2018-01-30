# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from collections import OrderedDict

from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.utils import is_managed


PROGRAM_STARTUP_ATTRIBUTE_TYPES = (
    ('django.forms.CharField', 'Text Line'),
    ('django.forms.IntegerField', 'Integer'),
    ('django.forms.FloatField', 'Floating Point Value'),
    ('django.forms.BooleanField', 'True/False'),
)


class ProgramStartupAttributeManager(models.Manager):

    def available(self, program):
        qs = self.get_queryset().filter(program__exact=program,
                                        staff_viewable=True)
        returnval = OrderedDict()
        for attr in qs:
            returnval[attr.get_field_name()] = attr
        return returnval


class ProgramStartupAttribute(MCModel):
    program = models.ForeignKey(Program)
    attribute_type = models.CharField(
        'Type',
        max_length=63,
        help_text='Select the type of information for this attribute',
        choices=PROGRAM_STARTUP_ATTRIBUTE_TYPES)
    attribute_label = models.CharField(
        'Label',
        max_length=127,
        help_text='Provide a human-readable label for this attribute.  '
        'It must be unique for the selected Program')
    attribute_description = models.CharField(
        'Description',
        max_length=255,
        help_text='Provide "help text" for this attribute',
        blank=True)
    admin_viewable = models.BooleanField(
        default=False,
        help_text='Can Startup Administrators view this attribute for '
        'their own Startups?')
    non_admin_viewable = models.BooleanField(
        default=False,
        help_text='Can Non-Startup Administrators view this attribute for '
        'their own Startups?')
    staff_viewable = models.BooleanField(
        default=False,
        help_text='Can MC Staff view this attribute?')
    finalist_viewable = models.BooleanField(
        default=False,
        help_text='Can Other Finalists view this attribute?')
    mentor_viewable = models.BooleanField(
        default=False,
        help_text='Can Mentors view this attribute?')

    objects = ProgramStartupAttributeManager()

    class Meta(MCModel.Meta):
        db_table = 'accelerator_programstartupattribute'
        managed = is_managed(db_table)
        ordering = ['program', 'attribute_label']
        unique_together = ('program', 'attribute_label')

    def __str__(self):
        tmpl = "%s (%s attribute)"
        return tmpl % (self.attribute_label, self.get_attribute_type_display())
