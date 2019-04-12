# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import UserRole
from impact.v1.events.base_user_role_grant_event import (
    BaseUserRoleGrantEvent,
)


class UserBecameFinalistEvent(BaseUserRoleGrantEvent):
    DESCRIPTION_FORMAT = "Became Finalist of {name} ({id})"
    EVENT_TYPE = "became finalist"
    USER_ROLE = UserRole.FINALIST

    def description(self):
        program = self.program_role_grant.program_role.program
        return self.DESCRIPTION_FORMAT.format(name=program.name,
                                              id=program.id)
