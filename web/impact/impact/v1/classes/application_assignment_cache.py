from impact.v1.classes.utils import collect_pairs
from accelerator.models import (
    ApplicationPanelAssignment,
    JUDGING_FEEDBACK_STATUS_INCOMPLETE,
)


class ApplicationAssignmentCache(object):
    def __init__(self):
        self._data = None

    def data(self, apps, feedback):
        if self._data is None:
            assignments = ApplicationPanelAssignment.objects.filter(
                application__in=apps).values_list(
                    "application_id",
                    "panel__judgepanelassignment__judge_id")
            finished_assignments = feedback.exclude(
                feedback_status=JUDGING_FEEDBACK_STATUS_INCOMPLETE
            ).values_list("application_id", "judge_id")
            self._data = collect_pairs(set(assignments) -
                                      set(finished_assignments))
        return self._data
