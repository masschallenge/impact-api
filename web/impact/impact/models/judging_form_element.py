# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.application_question import (
    ApplicationQuestion,
    TEXT_LIMIT_UNITS,
)
from impact.models.judging_form import JudgingForm
from impact.models.question import CHOICE_LAYOUTS
from impact.models.utils import is_managed


ELEMENT_TYPES = (('answer', 'Application Answer'),
                 ('boilerplate', 'Boilerplate'),
                 ('feedback', 'Feedback'))
FEEDBACK_TYPES = (('multiline', 'MultilineText'),
                  ('multichoice', 'MultipleChoice'),
                  ('number', 'Number'))
DASHBOARD_DISPLAY_VALUES = (('omit', 'Omit'),
                            ('value', 'Value'),
                            ('yesno', 'Yes/No'))
SHARING_VALUES = (('share-with-startup', 'Share with Startup'),
                  ('administrator-only', 'Share with Program Administrators'))


class JudgingFormElement(MCModel):
    form_type = models.ForeignKey(JudgingForm)
    element_number = models.IntegerField()
    element_name = models.CharField(max_length=50, blank=True)
    dashboard_label = models.CharField(max_length=50, blank=True)
    section_heading = models.CharField(max_length=40, blank=True)
    question_text = models.CharField(max_length=200, blank=True)
    help_text = models.CharField(max_length=1000, blank=True)
    element_type = models.CharField(
        max_length=64,
        choices=ELEMENT_TYPES,
    )
    feedback_type = models.CharField(
        max_length=64,
        choices=FEEDBACK_TYPES,
        blank=True,
    )
    display_value = models.CharField(
        max_length=64,
        choices=DASHBOARD_DISPLAY_VALUES,
    )
    score_element = models.BooleanField(default=False)
    mandatory = models.BooleanField(default=False)
    text_box_lines = models.IntegerField(null=True,
                                         default=0,
                                         blank=True)
    text_limit = models.IntegerField(null=True,
                                     default=0,
                                     blank=True)
    text_limit_units = models.CharField(
        max_length=64,
        choices=TEXT_LIMIT_UNITS,
        blank=True,
    )
    text_minimum = models.IntegerField(null=True,
                                       default=0,
                                       blank=True)
    text_minimum_units = models.CharField(
        max_length=64,
        choices=TEXT_LIMIT_UNITS,
        blank=True,
    )
    choice_options = models.CharField(max_length=200, blank=True)
    choice_layout = models.CharField(
        max_length=64,
        choices=CHOICE_LAYOUTS,
        blank=True,
    )
    application_question = models.ForeignKey(ApplicationQuestion,
                                             blank=True,
                                             null=True)
    sharing = models.CharField(
        max_length=64,
        choices=SHARING_VALUES,
        blank=True,
    )

    class Meta(MCModel.Meta):
        db_table = 'accelerator_judgingformelement'
        managed = is_managed(db_table)
        ordering = ['form_type', 'element_number', ]
        verbose_name_plural = 'Judging Form Elements'

    def __str__(self):
        return "Element %s (%s) from the %s" % (
            self.element_number, self.element_name, self.form_type.name)
