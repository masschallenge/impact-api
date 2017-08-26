from impact.models import UserRole
from impact.v1.events.base_user_role_grant_event import (
    BaseUserRoleGrantEvent,
)


class UserBecameConfirmedMentorEvent(BaseUserRoleGrantEvent):
    DESCRIPTION_FORMAT = "Became Confirmed Mentor for Program {name} ({id})"
    EVENT_TYPE = "became confirmed mentor"
    USER_ROLE = UserRole.MENTOR

    def description(self):
        program = self.program_role_grant.program_role.program
        return self.DESCRIPTION_FORMAT.format(name=program.name,
                                              id=program.id)
