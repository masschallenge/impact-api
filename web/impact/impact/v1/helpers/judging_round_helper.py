# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import re
from accelerator.models import JudgingRound
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
    STRING_FIELD,
)

JUDGING_ROUND_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "program_id": INTEGER_FIELD,
    "cycle_id": INTEGER_FIELD,
    "cycle_based_round": BOOLEAN_FIELD,
    "round_type": STRING_FIELD,  # ENUM

    # "start_date_time": STRING_FIELD,
    # "end_date_time": STRING_FIELD,
    # "application_type_id": INTEGER_FIELD,
    # "is_active": BOOLEAN_FIELD,
    # "buffer_before_event": INTEGER_FIELD,
    # "recruit_judges": STRING_FIELD,  # ENUM
    # "capture_capacity": BOOLEAN_FIELD,
    # "capacity_options": STRING_FIELD,  # '10|20|30|...'
    # "capture_availability": STRING_FIELD,
    # "feedback_display": STRING_FIELD,  # ENUM
    # "feedback_merge_with": INTEGER_FIELD,
    # "feedback_display_items": STRING_FIELD,  # ENUM
    # # In Person timing options
    # "presentation_mins": INTEGER_FIELD,
    # "buffer_mins": INTEGER_FIELD,
    # "break_mins": INTEGER_FIELD,
    # "num_breaks": INTEGER_FIELD,
    # "startup_label_id": INTEGER_FIELD,
    # "desired_judge_label_id": INTEGER_FIELD,
    # "confirmed_judge_label_id": INTEGER_FIELD,
}


class JudgingRoundHelper(ModelHelper):
    model = JudgingRound
    REQUIRED_KEYS = ["name", "program_id", "round_type"]
    OPTIONAL_KEYS = ["cycle_based_round"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    @classmethod
    def fields(cls):
        return JUDGING_ROUND_FIELDS
