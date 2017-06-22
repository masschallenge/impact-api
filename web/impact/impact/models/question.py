# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


CHOICE_LAYOUT_HORIZONTAL = "horizontal"
CHOICE_LAYOUT_VERTICAL = "vertical"
CHOICE_LAYOUT_DROPDOWN = "dropdown"

CHOICE_LAYOUTS = ((CHOICE_LAYOUT_HORIZONTAL, 'Horizontal'),
                  (CHOICE_LAYOUT_VERTICAL, 'Vertical'),
                  (CHOICE_LAYOUT_DROPDOWN, 'Dropdown'))

QUESTION_TYPE_MULTILINE = "multiline"
QUESTION_TYPE_MULTICHOICE = "multichoice"
QUESTION_TYPE_NUMBER = "number"

QUESTION_TYPES = ((QUESTION_TYPE_MULTILINE, 'MultilineText'),
                  (QUESTION_TYPE_MULTICHOICE, 'MultipleChoice'),
                  (QUESTION_TYPE_NUMBER, 'Number'))


class Question(MCModel):
    name = models.CharField(max_length=200)
    question_type = models.CharField(
        max_length=64,
        choices=QUESTION_TYPES,
    )
    choice_options = models.CharField(max_length=4000, blank=True)
    choice_layout = models.CharField(
        max_length=64,
        choices=CHOICE_LAYOUTS,
        blank=True,
    )

    class Meta(MCModel.Meta):
        db_table = 'mc_question'
        managed = is_managed(db_table)

    def __str__(self):
        return self.name
