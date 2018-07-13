# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import (
    Count,
    Sum,
)
from accelerator.models import Criterion

from impact.v1.helpers.model_helper import (
    REQUIRED_INTEGER_FIELD,
    ModelHelper,
    PK_FIELD,
    REQUIRED_STRING_FIELD,
)
ALL_FIELDS = {
    "id": PK_FIELD,
    "name": REQUIRED_STRING_FIELD,
    "type": REQUIRED_STRING_FIELD,
    "judging_round_id": REQUIRED_INTEGER_FIELD,
}


class CriterionHelper(ModelHelper):
    model = Criterion

    REQUIRED_KEYS = ["name",
                     "type",
                     "judging_round_id"]
    ALL_KEYS = REQUIRED_KEYS
    INPUT_KEYS = ALL_KEYS

    specific_helpers = {}

    @classmethod
    def register_helper(cls, klass, type, name):
        cls.specific_helpers[(type, name)] = klass

    @classmethod
    def find_helper(cls, type, name):
        return cls.specific_helpers.get((type, name), cls)

    def options(self, spec, apps):
        return [spec.option]

    def app_ids_for_feedback(self, feedbacks, option_name, **kwargs):
        return self.feedbacks_for_option(feedbacks, option_name).values_list(
            "application_id", flat=True)

    def app_count(self, apps, option_name):
        return apps.count()

    def total_capacity(self, commitments, option_name):
        return self.commitments_for_option(commitments, option_name).aggregate(
            total=Sum("capacity"))["total"]

    def remaining_capacity(self, commitments, assignments, option_name):
        judge_to_capacity = self.commitments_for_option(
            commitments, option_name).values_list("judge_id", "capacity")
        judge_to_count = self.count_assignments(assignments)
        result = 0
        for judge_id, capacity in judge_to_capacity:
            result += max(0, capacity - judge_to_count.get(judge_id, 0))
        return result

    def feedbacks_for_option(self, query, option_name):
        return self.query_for_option(query, option_name)

    def commitments_for_option(self, query, option_name):
        return self.query_for_option(query, option_name)

    def query_for_option(self, query, option_name):
        return query

    def count_assignments(self, assignments):
        results = {}
        for judge_id, assignment_count in assignments.annotate(
                assignment_count=Count("panel__applications")).values_list(
                    "judge_id", "assignment_count"):
            results[judge_id] = results.get(judge_id, 0) + assignment_count
        return results

    @classmethod
    def fields(cls):
        return ALL_FIELDS
