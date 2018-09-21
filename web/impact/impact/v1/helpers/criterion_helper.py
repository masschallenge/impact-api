# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import Sum

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
    application_field = "id"
    judge_field = "id"

    model = Criterion

    REQUIRED_KEYS = ["name",
                     "type",
                     "judging_round_id"]
    CLASS_TO_FIELD = {}
    ALL_KEYS = REQUIRED_KEYS
    INPUT_KEYS = ALL_KEYS

    specific_helpers = {}

    @classmethod
    def register_helper(cls, klass, type, name):
        cls.specific_helpers[(type, name)] = klass

    @classmethod
    def find_helper(cls, criterion):
        return cls.specific_helpers.get((criterion.type, criterion.name),
                                        cls)(criterion)

    def options(self, spec, apps):
        return [spec.option]

    def app_ids_for_feedbacks(self, feedbacks, option_name, **kwargs):
        return self.filter_by_judge_option(feedbacks, option_name).values_list(
            "application_id", flat=True)

    def app_count(self, apps, option_name):
        return apps.count()

    def total_capacity(self, commitments, option_name):
        return self.filter_by_judge_option(commitments, option_name).aggregate(
            total=Sum("capacity"))["total"]

    def remaining_capacity(self, commitments, assignment_counts, option_name):
        judge_to_capacity = self.filter_by_judge_option(
            commitments, option_name).values_list("judge_id", "capacity")
        result = 0
        for judge_id, capacity in judge_to_capacity:
            result += max(0, capacity - assignment_counts.get(judge_id, 0))
        return result

    def filter_by_judge_option(self, query, option_name):
        return query

    @classmethod
    def clone_criteria(cls, source_judging_round_id, target_judging_round_id):

        cls.delete_existing_criteria(target_judging_round_id)
        criteria = cls.model.objects.filter(
            judging_round_id=source_judging_round_id)
        return [cls.clone_criterion(criterion, target_judging_round_id)
                for criterion in criteria]

    @classmethod
    def delete_existing_criteria(cls, judging_round_id):
        criteria = cls.model.objects.filter(judging_round_id=judging_round_id)
        for criterion in criteria:
            criterion.criterionoptionspec_set.all().delete()
        criteria.delete()

    @classmethod
    def fields(cls):
        return ALL_FIELDS

    @classmethod
    def clone_criterion(cls, criterion, target_judging_round_id):
        clone = cls.model.objects.create(
            judging_round_id=target_judging_round_id,
            type=criterion.type,
            name=criterion.name)
        return criterion.pk, clone.pk

    def option_for_field(self, field):
        return ""

    def field_matches_option(self, field, option):
        return True
