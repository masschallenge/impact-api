from impact.models import (
    ProgramCycle,
    SUBMITTED_APP_STATUS,
)


class OrganizationBecomeEntrantEvent(object):
    DESCRIPTION_FORMAT = "Applied to {}"
    EVENT_TYPE = "become entrant"

    def __init__(self, application):
        self.application = application

    @classmethod
    def events(cls, organization):
        result = []
        for startup in organization.startup_set.all():
            entrant_app_types = [cycle.default_application_type for
                                 cycle in ProgramCycle.objects.all()]
            for app in startup.application_set.filter(
                    application_type__in=entrant_app_types,
                    application_status=SUBMITTED_APP_STATUS):
                result.append(cls(app))
        return result

    def serialize(self):
        submission_time = self._submission_datetime()
        return {
            "datetime": submission_time,
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(
                self.application.cycle.name)
            }

    def _submission_datetime(self):
        result = self.application.submission_datetime
        if result is None:
            return self.cycle.application_final_deadline_date
        return result
