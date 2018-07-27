from impact.v1.classes.utils import collect_pairs
from impact.v1.helpers import CriterionHelper
from accelerator.models import (
    ApplicationPanelAssignment,
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JUDGING_FEEDBACK_STATUS_INCOMPLETE,
)

class ApplicationDataCache(object):
    def __init__(self):
        self._data = None

    def data(self, criteria, apps, feedback):
        if self._data is None:
            fields = set(["id"])
            self._data = {}
            for criterion in criteria:
                helper = CriterionHelper.find_helper(criterion)
                fields.add(helper.application_field)
            assignment_data = self._assignment_data(apps, feedback)
            read_data = self._read_data(feedback)
            for field_data in apps.values(*list(fields)):
                app_id = field_data["id"]
                self._data[app_id] = {
                    "assignments": assignment_data.get(app_id, []),
                    "feedbacks": read_data.get(app_id, []),
                    "fields": field_data,
                }
        return self._data

    def _assignment_data(self, apps, feedback):
        assignments = ApplicationPanelAssignment.objects.filter(
            application__in=apps).values_list(
                "application_id",
                "panel__judgepanelassignment__judge_id")
        finished_assignments = feedback.exclude(
            feedback_status=JUDGING_FEEDBACK_STATUS_INCOMPLETE
        ).values_list("application_id", "judge_id")
        return collect_pairs(set(assignments) - set(finished_assignments))

    def _read_data(self, feedback):
        app_to_judge = feedback.filter(
            feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE).values_list(
                "application_id", "judge_id")
        return collect_pairs(app_to_judge)
