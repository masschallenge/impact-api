from datetime import datetime
from pytz import utc
from django.db.models import Q
from impact.models import (
    ProgramCycle,
    SUBMITTED_APP_STATUS,
    StartupRole,
    StartupStatus,
)
from impact.utils import (
    DAWN_OF_TIME,
    next_instance,
    previous_instance,
)


class OrganizationBecameEntrantEvent(object):
    DESCRIPTION_FORMAT = "Applied to {}"
    EVENT_TYPE = "became entrant"

    def __init__(self, application):
        self.application = application
        self.startup = self.application.startup
        self.cycle = self.application.cycle
        self.startup_status = StartupStatus.objects.filter(
            program_startup_status__startup_role__name=StartupRole.ENTRANT,
            program_startup_status__program__cycle=self.cycle,
            startup=self.startup).order_by("created_at").first()

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
        earliest, latest = self._datetimes()
        return {
            "cycle": self.cycle.name,
            "cycle_id": self.cycle.id,
            "programs": self._program_data(),
            "datetime": earliest,
            "latest_datetime": latest,
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(
                self.application.cycle.name)
            }

    def _datetimes(self):
        return (self._startup_status_time() or
                self._submission_datetime() or
                self._application_final_deadline() or
                self._infer_datetimes())

    def _startup_status_time(self):
        if self.startup_status and self.startup_status.created_at is not None:
            return (self.startup_status.created_at,
                    self.startup_status.created_at)
        return None

    def _submission_datetime(self):
        result = self.application.submission_datetime
        if result is not None:
            return (result, result)
        return None

    def _application_final_deadline(self):
        cycle = self.application.cycle
        result = cycle.application_final_deadline_date
        if result is not None:
            return (result, result)
        return None

    def _infer_datetimes(self):
        earliest = DAWN_OF_TIME
        cycle = self.application.cycle
        query = Q(application_final_deadline_date__isnull=False)
        prev_cycle = previous_instance(cycle, query)
        if prev_cycle:
            earliest = prev_cycle.application_final_deadline_date
        latest = utc.localize(datetime.now())
        next_cycle = next_instance(cycle, query)
        if next_cycle:
            latest = next_cycle.application_final_deadline_date
        return (earliest, latest)

    def _program_data(self):
        raw_data = self.startup.startupprograminterest_set.filter(
            applying=True,
            program__cycle=self.cycle
            ).order_by("order").values_list("program_id",
                                            "program__name")
        result = []
        preference = 1
        for id, name in raw_data:
            result.append({"id": id,
                           "name": name,
                           "preference": preference})
            preference += 1
        return result
