from impact.models import StartupRole
from impact.utils import compose_filter


class OrganizationBecameFinalistEvent(object):
    DESCRIPTION_FORMAT = "Became Finalist for {}"
    EVENT_TYPE = "became finalist"

    def __init__(self, startup_status):
        self.startup_status = startup_status

    @classmethod
    def events(cls, organization):
        result = []
        for startup in organization.startup_set.all():
            for ss in startup.startupstatus_set.filter(**compose_filter(
                    ["program_startup_status",
                     "startup_role",
                     "name"],
                    StartupRole.FINALIST)):
                result.append(cls(ss))
        return result

    def serialize(self):
        finalist_time = self._finalist_datetime()
        program = self.startup_status.program_startup_status.program
        return {
            "cycle": program.cycle.name,
            "cycle_id": program.cycle.id,
            "datetime": finalist_time,
            "description": self.DESCRIPTION_FORMAT.format(
                self.startup_status.program_startup_status.program.name),
            "event_type": self.EVENT_TYPE,
            "program": program.name,
            "program_id": program.id,
            }

    def _finalist_datetime(self):
        result = self.startup_status.created_at
        if result is None:
            program = self.startup_status.program_startup_status.program
            return program.start_date
        return result
