from impact.models import UserRole
from impact.utils import compose_filter


class UserBecameFinalistEvent(object):
    DESCRIPTION_FORMAT = "Became Finalist of {}"
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
        finalist_time = self._finalist_datetime()
        return {
            "datetime": finalist_time,
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(
                self.program_role_grant.program_role.program.name)
            }

    def _finalist_datetime(self):
        result = self.program_role_grant.created_at
        if result is None:
            program = self.program_role_grant.program_role.program
            return program.start_date
        return result
