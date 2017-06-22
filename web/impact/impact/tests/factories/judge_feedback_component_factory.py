# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import (
    JudgeFeedbackComponent,
)

from .judge_application_feedback_factory import (
    JudgeApplicationFeedbackFactory,
)
from .judging_form_element_factory import JudgingFormElementFactory


class JudgeFeedbackComponentFactory(DjangoModelFactory):

    class Meta:
        model = JudgeFeedbackComponent

    judge_feedback = SubFactory(JudgeApplicationFeedbackFactory)
    feedback_element = SubFactory(JudgingFormElementFactory)
    answer_text = Sequence(lambda n: "Judge Answer Text {0}".format(n))
