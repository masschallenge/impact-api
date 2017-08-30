# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from impact.models import (
    CAPTURE_AVAILABILITY_DISABLED,
    DEFAULT_BUFFER_BEFORE_EVENT,
    FEEDBACK_DISPLAY_DISABLED,
    IN_PERSON_JUDGING_ROUND_TYPE,
    JudgingRound,
    RECRUIT_NONE,
)
from impact.tests.utils import months_from_now

from .application_type_factory import ApplicationTypeFactory
from .judging_form_factory import JudgingFormFactory
from .program_factory import ProgramFactory
from .startup_label_factory import StartupLabelFactory
from .user_label_factory import UserLabelFactory


class JudgingRoundFactory(DjangoModelFactory):

    class Meta:
        model = JudgingRound

    program = SubFactory(ProgramFactory)
    cycle_based_round = False
    name = Sequence(lambda n: "name{0}".format(n))
    start_date_time = months_from_now(1)
    end_date_time = months_from_now(2)
    is_active = True
    round_type = IN_PERSON_JUDGING_ROUND_TYPE
    application_type = SubFactory(ApplicationTypeFactory)
    buffer_before_event = DEFAULT_BUFFER_BEFORE_EVENT
    judging_form = SubFactory(JudgingFormFactory)
    recruit_judges = RECRUIT_NONE
    recruiting_prompt = ""
    positive_recruiting_prompt = ""
    negative_recruiting_prompt = ""
    capture_capacity = False
    capacity_prompt = ""
    capacity_options = "10|20|30|40|50|60|70|80"
    capture_availability = CAPTURE_AVAILABILITY_DISABLED
    feedback_display = FEEDBACK_DISPLAY_DISABLED
    feedback_merge_with = None
    feedback_display_message = ""
    feedback_display_items = ""
    judge_instructions = ""
    presentation_mins = 20
    buffer_mins = 10
    break_mins = 10
    num_breaks = 1
    startup_label = SubFactory(StartupLabelFactory)
    desired_judge_label = SubFactory(UserLabelFactory)
    confirmed_judge_label = SubFactory(UserLabelFactory)
