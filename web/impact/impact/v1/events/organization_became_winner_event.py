# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ...utils import compose_filter
from .base_history_event import BaseHistoryEvent
from ..helpers import (
    OPTIONAL_INTEGER_FIELD,
    OPTIONAL_STRING_FIELD,
)


class OrganizationBecameWinnerEvent(BaseHistoryEvent):
    DESCRIPTION_FORMAT = "Became Winner for {}"
    EVENT_TYPE = "became winner"

    CLASS_FIELDS = {
        "cycle": OPTIONAL_STRING_FIELD,
        "cycle_id": OPTIONAL_INTEGER_FIELD,
        "program": OPTIONAL_STRING_FIELD,
        "program_id": OPTIONAL_INTEGER_FIELD,
        "winner_level": OPTIONAL_STRING_FIELD,
        "winner_level_name": OPTIONAL_STRING_FIELD,
    }

    def __init__(self, startup_status):
        super().__init__()
        self._program = startup_status.program_startup_status.program
        self.startup_status = startup_status

    @classmethod
    def events(cls, organization):
        result = []
        for startup in organization.startups.all():
            for ss in startup.startupstatus_set.filter(**compose_filter(
                    ["program_startup_status",
                     "startup_role",
                     "name",
                     "icontains"],
                    "winner")):
                result.append(cls(ss))
        return result

    def calc_datetimes(self):
        self.earliest = (self.startup_status.created_at
                         or self._program.end_date)

    def description(self):
        return self.DESCRIPTION_FORMAT.format(
            self.startup_status.program_startup_status.program.name)

    def cycle(self):
        return self._program.cycle.name

    def cycle_id(self):
        return self._program.cycle.id

    def program(self):
        return self._program.name

    def program_id(self):
        return self._program.id

    def winner_level(self):
        return self.startup_status.program_startup_status.startup_role.name

    def winner_level_name(self):
        pss = self.startup_status.program_startup_status
        program = pss.program.name
        winner_level = pss.startup_role.name
        return '{} {}'.format(program, winner_level)
