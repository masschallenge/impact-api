# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .base_user_role_grant_event import BaseUserRoleGrantEvent


class BaseUserBecameMentorEvent(BaseUserRoleGrantEvent):
    DESCRIPTION_FORMAT = "Became {role_name} for Program {name} ({id})"

    def description(self):
        program = self.program_role_grant.program_role.program
        return self.DESCRIPTION_FORMAT.format(role_name=self.ROLE_NAME,
                                              name=program.name,
                                              id=program.id)
