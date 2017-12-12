# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import (
    ABCMeta,
    abstractmethod,
)
from impact.models import UserRole
from impact.v1.events.base_user_role_grant_event import (
    BaseUserRoleGrantEvent,
)
from impact.v1.helpers import (
    INTEGER_FIELD,
    STRING_FIELD,
)


class BaseUserBecameJudgeEvent(BaseUserRoleGrantEvent):
    __metaclass__ = ABCMeta

    PROGRAM_ROLE_FORMAT = "Granted {user_role} Program Role {name} ({id})"
    JUDGING_ROUND_FORMAT = "{user_role} for Judging Round {name} ({id})"

    CLASS_FIELDS = {
        "judging_round_id": INTEGER_FIELD,
        "judging_round_name": STRING_FIELD,
        }

    def __init__(self, program_role_grant):
        super().__init__(program_role_grant)
        label = program_role_grant.program_role.user_label
        self.judging_round = self.judging_round_from_label(label)

    @abstractmethod
    def judging_round_from_label(self, label):
        pass  # pragma: no cover

    def description(self):
        if self.judging_round:
            return self.JUDGING_ROUND_FORMAT.format(
                user_role=self.USER_ROLE,
                name=self.judging_round.short_name(),
                id=self.judging_round.id)
        program_role = self.program_role_grant.program_role
        return self.PROGRAM_ROLE_FORMAT.format(
            user_role=self.USER_ROLE,
            name=program_role.name,
            id=program_role.id)

    def judging_round_id(self):
        if self.judging_round:
            return self.judging_round.id

    def judging_round_name(self):
        if self.judging_round:
            return self.judging_round.short_name()
