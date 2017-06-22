# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.application_type import ApplicationType
from impact.models.program import Program
from impact.models.question import (
    CHOICE_LAYOUTS,
    QUESTION_TYPES,
    Question,
)
from impact.models.utils import is_managed


TEXT_LIMIT_UNITS = (('characters', 'Characters'),
                    ('words', 'Words'))


class ApplicationQuestion(MCModel):
    application_type = models.ForeignKey(ApplicationType)
    program = models.ForeignKey(Program,
                                blank=True,
                                null=True)
    question_number = models.IntegerField()
    section_heading = models.CharField(max_length=40, blank=True)
    question_text = models.CharField(max_length=200, blank=True)
    help_text = models.CharField(max_length=1000, blank=True)
    # To be removed:
    question_type = models.CharField(
        max_length=64,
        choices=QUESTION_TYPES,
    )
    mandatory = models.BooleanField(default=False)
    text_box_lines = models.IntegerField(blank=True)
    text_limit = models.IntegerField(blank=True)
    text_limit_units = models.CharField(
        max_length=64,
        choices=TEXT_LIMIT_UNITS,
        blank=True,
    )
    # To be removed:
    choice_options = models.CharField(max_length=4000, blank=True)
    # To be removed:
    choice_layout = models.CharField(
        max_length=64,
        choices=CHOICE_LAYOUTS,
        blank=True,
    )
    question = models.ForeignKey(Question, blank=True, null=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_applicationquestion'
        managed = is_managed(db_table)
        ordering = ['application_type', 'question_number', ]
        verbose_name_plural = 'Application Questions'

    def __str__(self):
        return "Question %s (%s) from the %s" % (
            self.question_number,
            self.question_text[:10],
            self.application_type.name)
