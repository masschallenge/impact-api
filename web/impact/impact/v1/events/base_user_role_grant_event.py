from datetime import datetime
from impact.models import (
    ProgramRoleGrant,
    UserRole,
)
from impact.utils import compose_filter


class BaseUserRoleGrantEvent(object):

    def __init__(self, program_role_grant):
        self.program_role_grant = program_role_grant

    @classmethod
    def events(cls, user):
        result = []
        for prg in user.programrolegrant_set.filter(**compose_filter(
                ["program_role",
                 "user_role",
                 "name"],
                cls.USER_ROLE)):
            result.append(cls(prg))
        return result

    def serialize(self):
        earliest, latest = self._user_event_datetime()
        return {
            "datetime": earliest,
            "latest_datetime": latest,
            "event_type": self.EVENT_TYPE,
            "description": self.description(),
            }

    def _user_event_datetime(self):
        result = self.program_role_grant.created_at
        if result:
            return (result, result)
        program = self.program_role_grant.program_role.program
        earliest = max(program.start_date,
                       self.program_role_grant.person.date_joined)
        latest = datetime.now()
        prg_with_created_at = ProgramRoleGrant.objects.filter(
            id__gt=self.program_role_grant.id,
            created_at__isnull=False).order_by("id").first()
        if prg_with_created_at:
            latest = prg_with_created_at.created_at
        return (earliest, latest)
