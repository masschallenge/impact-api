from collections import defaultdict
from datetime import datetime
from pytz import utc

from impact.v1.classes.utils import collect_pairs
from accelerator.models import (
    ApplicationPanelAssignment,
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JUDGING_FEEDBACK_STATUS_INCOMPLETE,
)


class ApplicationDataCache(object):
    def __init__(self, apps, criteria, feedback, criterion_helpers):
        self.apps = apps
        self.criteria = criteria
        self.feedback = feedback
        self.data = {}
        fields = set(["id"])
        self.criterion_helpers = criterion_helpers
        for helper in self.criterion_helpers:
            fields.add(helper.application_field)
        assignment_data = self._assignment_data()
        assignment_ages = self._application_assignment_ages()
        read_data = self._read_data()
        for field_data in apps.values(*list(fields)):
            app_id = field_data["id"]
            self.data[app_id] = {
                "assignments": assignment_data.get(app_id, []),
                "feedbacks": read_data.get(app_id, []),
                "fields": field_data,
                "assignment_ages": assignment_ages[app_id]
            }

    def _assignment_data(self):
        assignments = ApplicationPanelAssignment.objects.filter(
            application__in=self.apps).values_list(
                "application_id",
                "panel__judgepanelassignment__judge_id")
        finished_assignments = self.feedback.exclude(
            feedback_status=JUDGING_FEEDBACK_STATUS_INCOMPLETE
        ).values_list("application_id", "judge_id")
        return collect_pairs(set(assignments) - set(finished_assignments))

    def _read_data(self):
        app_to_judge = self.feedback.filter(
            feedback_status=JUDGING_FEEDBACK_STATUS_COMPLETE).values_list(
                "application_id", "judge_id")
        return collect_pairs(app_to_judge)

    def _application_assignment_ages(self):
        now = utc.localize(datetime.utcnow())
        app_ages_dict = defaultdict(dict)
        assignment_ages = ApplicationPanelAssignment.objects.filter(
            application__in=self.apps).values_list(
                "application_id",
                "panel__judgepanelassignment__judge_id",
                "created_at")
        for app_id, judge_id, created_at in assignment_ages:
            app_ages_dict[app_id][judge_id] = (now - created_at).total_seconds()
        return app_ages_dict
