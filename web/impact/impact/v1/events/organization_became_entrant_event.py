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
from impact.v1.events.base_history_event import BaseHistoryEvent
from impact.v1.helpers import (
    INTEGER_FIELD,
    STRING_FIELD,
)

PROGRAMS_FIELD = {
    "json-schema": {
        "type": "array",
        "item": {
            "type": "object",
            "properties": {
                "id": INTEGER_FIELD,
                "name": STRING_FIELD,
                "preference": INTEGER_FIELD,
            },
        },
    },
}


class OrganizationBecameEntrantEvent(BaseHistoryEvent):
    DESCRIPTION_FORMAT = "Applied to {}"
    EVENT_TYPE = "became entrant"

    CLASS_FIELDS = {
        "cycle_id": INTEGER_FIELD,
        "cycle": STRING_FIELD,
        "programs": PROGRAMS_FIELD,
       }

    def __init__(self, application):
        super().__init__()
        self.application = application
        self.startup = self.application.startup
        self._cycle = self.application.cycle
        self.startup_status = StartupStatus.objects.filter(
            program_startup_status__startup_role__name=StartupRole.ENTRANT,
            program_startup_status__program__cycle=self._cycle,
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

    def cycle(self):
        return self._cycle.name

    def cycle_id(self):
        return self._cycle.id

    def programs(self):
        raw_data = self.startup.startupprograminterest_set.filter(
            applying=True,
            program__cycle=self._cycle
            ).order_by("order").values_list("program_id",
                                            "program__name")
        result = []
        preference = 1
        for pk, name in raw_data:
            result.append({"id": pk,
                           "name": name,
                           "preference": preference})
            preference += 1
        return result

    def description(self):
        return self.DESCRIPTION_FORMAT.format(self.application.cycle.name)

    def calc_datetimes(self):
        return (self._startup_status_time() or
                self._submission_datetime() or
                self._application_final_deadline() or
                self._infer_datetimes())

    def _startup_status_time(self):
        if self.startup_status:
            self.earliest = self.startup_status.created_at
        return self.earliest is not None

    def _submission_datetime(self):
        self.earliest = self.application.submission_datetime
        return self.earliest is not None

    def _application_final_deadline(self):
        cycle = self.application.cycle
        self.earliest = cycle.application_final_deadline_date
        return self.earliest is not None

    def _infer_datetimes(self):
        self.earliest = DAWN_OF_TIME
        cycle = self.application.cycle
        query = Q(application_final_deadline_date__isnull=False)
        prev_cycle = previous_instance(cycle, query)
        if prev_cycle:
            self.earliest = prev_cycle.application_final_deadline_date
        self.latest = utc.localize(datetime.now())
        next_cycle = next_instance(cycle, query)
        if next_cycle:
            self.latest = next_cycle.application_final_deadline_date
        return True
