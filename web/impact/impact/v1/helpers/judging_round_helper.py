# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import JudgingRound
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    OPTIONAL_INTEGER_FIELD,
    ModelHelper,
    OPTIONAL_STRING_FIELD,
    PK_FIELD,
    READ_ONLY_STRING_FIELD,
    REQUIRED_STRING_FIELD,
)

JUDGING_ROUND_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "is_active": BOOLEAN_FIELD,
    "full_name": READ_ONLY_STRING_FIELD,
    "round_type": OPTIONAL_STRING_FIELD,
    "cycle_based_round": BOOLEAN_FIELD,
    "program_id": OPTIONAL_INTEGER_FIELD,
    "cycle_id": OPTIONAL_INTEGER_FIELD,
    # The next two fields should have a date validator.  See AC-5806.
    "start_date_time": OPTIONAL_STRING_FIELD,
    "end_date_time": OPTIONAL_STRING_FIELD,
}


class JudgingRoundHelper(ModelHelper):
    model = JudgingRound
    REQUIRED_KEYS = ["name", "program_id", "round_type"]
    OPTIONAL_KEYS = ["cycle_based_round"]
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    @classmethod
    def fields(cls):
        return JUDGING_ROUND_FIELDS

    @property
    def full_name(self):
        # JudgingRounds in django-accelerator currently have both a
        # short_name and a display_name.  However, the display_name
        # appears to be simpler and not well justified.  Specifically
        # it does not list all of the program abbreviations for
        # cycle-base rounds.  For example, for judging round 48, the
        # display_name is currently "2017-04 BOS Round 1", but the
        # short_name is "2017-04 BOS CH IL Round 1".  See ticket
        # AC-5694 for proposed cleanup.
        return self.subject.short_name()
