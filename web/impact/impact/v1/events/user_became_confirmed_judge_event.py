# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models import UserRole
from impact.v1.events.base_user_role_grant_event import (
    BaseUserRoleGrantEvent,
)
from impact.v1.helpers import (
    INTEGER_FIELD,
    STRING_FIELD,
)


class UserBecameConfirmedJudgeEvent(BaseUserRoleGrantEvent):
    PROGRAM_ROLE_FORMAT = "Granted Confirmed Judge Program Role {name} ({id})"
    JUDGING_ROUND_FORMAT = "Confirmed as Judge for Judging Round {name} ({id})"
    EVENT_TYPE = "became confirmed judge"
    USER_ROLE = UserRole.JUDGE

    CLASS_FIELDS = {
        "judging_round_id": INTEGER_FIELD,
        "judging_round_name": STRING_FIELD,
        }

    def __init__(self, program_role_grant):
        super().__init__(program_role_grant)
        self.judging_round = None
        label = program_role_grant.program_role.user_label
        if label:
            self.judging_round = label.rounds_confirmed_for.first()

    def description(self):
        if self.judging_round:
            return self.JUDGING_ROUND_FORMAT.format(
                name=self.judging_round.short_name(),
                id=self.judging_round.id)
        program_role = self.program_role_grant.program_role
        return self.PROGRAM_ROLE_FORMAT.format(
            name=program_role.name,
            id=program_role.id)

    def judging_round_id(self):
        if self.judging_round:
            return self.judging_round.id

    def judging_round_name(self):
        if self.judging_round:
            return self.judging_round.short_name()
