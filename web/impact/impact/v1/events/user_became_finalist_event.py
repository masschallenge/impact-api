from datetime import datetime
from impact.models import (
    ProgramRoleGrant,
    UserRole,
)
from impact.utils import compose_filter


class UserBecameFinalistEvent(object):
    DESCRIPTION_FORMAT = "Became Finalist of {name} ({id})"
    EVENT_TYPE = "became finalist"

    def __init__(self, program_role_grant):
        self.program_role_grant = program_role_grant

    @classmethod
    def events(cls, user):
        result = []
        for prg in user.programrolegrant_set.filter(**compose_filter(
                ["program_role",
                 "user_role",
                 "name"],
                UserRole.FINALIST)):
            result.append(cls(prg))
        return result

    def serialize(self):
        earliest, latest = self._finalist_datetime()
        program = self.program_role_grant.program_role.program
        return {
            "datetime": earliest,
            "latest_datetime": latest,
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(name=program.name,
                                                          id=program.id)
            }

    def _finalist_datetime(self):
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
