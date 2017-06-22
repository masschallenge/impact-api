# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import (
    JUDGING_STATUS_NO_CONFLICT,
    JudgeApplicationFeedback,
)

from .application_factory import ApplicationFactory
from .expert_factory import ExpertFactory
from .judging_form_factory import JudgingFormFactory
from .panel_factory import PanelFactory


class JudgeApplicationFeedbackFactory(DjangoModelFactory):
    class Meta:
        model = JudgeApplicationFeedback

    application = SubFactory(ApplicationFactory)
    form_type = SubFactory(JudgingFormFactory)
    judge = SubFactory(ExpertFactory)
    panel = SubFactory(PanelFactory)
    judging_status = JUDGING_STATUS_NO_CONFLICT
    # feedback_status is a post_save calculated field.
