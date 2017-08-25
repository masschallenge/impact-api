from impact.models import (
    StartupRole,
    StartupStatus,    
)


class OrganizationBecomeFinalistEvent(object):
    DESCRIPTION_FORMAT = "Became Finalist on {}"
    EVENT_TYPE = "become finalist"

    def __init__(self, startup_status):
        self.startup_status = startup_status

    @classmethod
    def events(cls, organization):
        result = []
        for startup in organization.startup_set.all():
            for ss in startup.startupstatus_set.filter(
                    program_startup_status__startup_role__name=StartupRole.FINALIST):
                result.append(cls(ss))
        return result

    def serialize(self):
        finalist_time = self._finalist_datetime()
        return {
            "datetime": finalist_time,
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(
                self.startup_status.program_startup_status.program.name)
            }

    def _finalist_datetime(self):
        result = self.startup_status.created_at
        if result is None:
            return self.startup_status.program_startup_status.program.start_date
        return result
