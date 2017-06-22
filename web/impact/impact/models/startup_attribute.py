# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_startup_attribute import ProgramStartupAttribute
from impact.models.startup import Startup
from impact.models.utils import is_managed


class StartupAttribute(MCModel):
    startup = models.ForeignKey(Startup)
    attribute = models.ForeignKey(ProgramStartupAttribute)
    # TextField allows me to ignore max_length.
    attribute_value = models.TextField(
        'Value',
        help_text='Stored text representation of the value')

    class Meta(MCModel.Meta):
        db_table = 'mc_startupattribute'
        managed = is_managed(db_table)
        verbose_name_plural = 'Startup Attributes'

    @property
    def field_name(self):
        """it is important that this return a unique value per form instance
        """
        return self.attribute.get_field_name()

    @field_name.setter
    def field_name(self, value):
        """cannot set field_name"""
        pass

    @property
    def value(self):
        return self.attribute.convert_to_field_value(self.attribute_value)

    @value.setter
    def value(self, value):
        self.attribute_value = self.attribute.convert_to_stored_value(value)
