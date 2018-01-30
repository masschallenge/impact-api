# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import StartupRole
from impact.utils import compose_filter
from impact.v1.events.base_history_event import BaseHistoryEvent
from impact.v1.helpers import (
    INTEGER_FIELD,
    STRING_FIELD,
)


class OrganizationBecameFinalistEvent(BaseHistoryEvent):
    DESCRIPTION_FORMAT = "Became Finalist for {}"
    EVENT_TYPE = "became finalist"

    CLASS_FIELDS = {
        "cycle": STRING_FIELD,
        "cycle_id": INTEGER_FIELD,
        "program": STRING_FIELD,
        "program_id": INTEGER_FIELD,
    }

    def __init__(self, startup_status):
        super().__init__()
        self.startup_status = startup_status
        self._program = self.startup_status.program_startup_status.program

    @classmethod
    def events(cls, organization):
        result = []
        for startup in organization.startup_set.all():
            for ss in startup.startupstatus_set.filter(**compose_filter(
                    ["program_startup_status",
                     "startup_role",
                     "name"],
                    StartupRole.FINALIST)):
                result.append(cls(ss))
        return result

    def calc_datetimes(self):
        self.earliest = self.startup_status.created_at
        if self.earliest is None:
            self.earliest = self._program.start_date

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
