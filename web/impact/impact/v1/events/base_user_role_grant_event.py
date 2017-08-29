from abc import (
    ABCMeta,
    abstractmethod,
)
from datetime import datetime
from pytz import utc
from impact.models import ProgramRoleGrant
from impact.utils import compose_filter


class BaseUserRoleGrantEvent(object):
    __metaclass__ = ABCMeta

    def __init__(self, program_role_grant):
        self.program_role_grant = program_role_grant

    @abstractmethod
    def description(self):
        pass  # pragma: no cover

    @classmethod
    def events(cls, user):
        result = []
        user_role_name_filter = compose_filter(
            ["program_role", "user_role", "name"],
            cls.USER_ROLE)
        for prg in user.programrolegrant_set.filter(**user_role_name_filter):
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
        earliest = max(program.cycle.application_final_deadline_date,
                       self.program_role_grant.person.date_joined)
        latest = utc.localize(datetime.now())
        prg_with_created_at = ProgramRoleGrant.objects.filter(
            id__gt=self.program_role_grant.id,
            created_at__isnull=False).order_by("id").first()
        if prg_with_created_at:
            latest = prg_with_created_at.created_at
        return (earliest, latest)
