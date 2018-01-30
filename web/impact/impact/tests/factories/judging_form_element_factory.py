# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import JudgingFormElement

from .application_question_factory import ApplicationQuestionFactory
from .judging_form_factory import JudgingFormFactory


class JudgingFormElementFactory(DjangoModelFactory):

    class Meta:
        model = JudgingFormElement

    form_type = SubFactory(JudgingFormFactory)
    element_number = Sequence(lambda n: n)
    element_name = Sequence(lambda n: "Judging Form Element {0}".format(n))
    dashboard_label = ""
    section_heading = ""
    question_text = Sequence(lambda n: "Judging Form Question {0}".format(n))
    help_text = ""
    element_type = "answer"
    feedback_type = ""
    display_value = "value"
    mandatory = False
    text_box_lines = 0
    text_limit = 0
    text_limit_units = ""
    text_minimum = 0
    text_minimum_units = 0
    choice_options = ""
    choice_layout = ""
    application_question = SubFactory(ApplicationQuestionFactory)
    sharing = ""
