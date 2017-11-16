# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import (
    ABCMeta,
    abstractmethod,
)
from datetime import datetime
from pytz import utc
from django.db.models import Q
from impact.utils import (
    compose_filter,
    next_instance,
)
from impact.v1.events.base_history_event import BaseHistoryEvent
from impact.v1.helpers import (
    INTEGER_FIELD,
    STRING_FIELD,
)


class BaseUserRoleGrantEvent(BaseHistoryEvent):
    __metaclass__ = ABCMeta

    CLASS_FIELDS = {
        "cycle_id": INTEGER_FIELD,
        "cycle": STRING_FIELD,
        "program_id": INTEGER_FIELD,
        "program": STRING_FIELD,
       }

    @classmethod
    def events(cls, user):
        result = []
        user_role_name_filter = compose_filter(
            ["program_role", "user_role", "name"],
            cls.USER_ROLE)
        for prg in user.programrolegrant_set.filter(**user_role_name_filter):
            result.append(cls(prg))
        return result

    def __init__(self, program_role_grant):
        super().__init__()
        self.program_role_grant = program_role_grant
        self._program = program_role_grant.program_role.program

    @abstractmethod
    def description(self):
        pass  # pragma: no cover

    def cycle(self):
        return self._program.cycle.name

    def cycle_id(self):
        return self._program.cycle.id

    def program(self):
        return self._program.name

    def program_id(self):
        return self._program.id

    def calc_datetimes(self):
        result = self.program_role_grant.created_at
        if result:
            self.earliest = result
            self.latest = result
            return
        self.earliest = self.program_role_grant.person.date_joined
        deadline = self._program.cycle.application_final_deadline_date
        if deadline and deadline > self.earliest:
            self.earliest = deadline
        self.latest = utc.localize(datetime.now())
        prg_with_created_at = next_instance(self.program_role_grant,
                                            Q(created_at__isnull=False))
        if prg_with_created_at:
            self.latest = prg_with_created_at.created_at
