# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

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
    '''Encapsulates business logic for Criteria, including logic
    around allocation, analysis, and cloning.
    The CriterionHelper superclass counts judges without regard to any
    features. Therefore it is a suitable class to use for the "reads"
    criterion.
    '''

    application_field = "id"
    judge_field = cache_judge_field = "id"
    cache_key = "reads"

    model = Criterion

    REQUIRED_KEYS = ["name",
                     "type",
                     "judging_round_id"]
    CLASS_TO_FIELD = {}
    ALL_KEYS = REQUIRED_KEYS
    INPUT_KEYS = ALL_KEYS

    specific_helpers = {}

    def __init__(self, subject):
        super().__init__(subject)
        self.subject = subject
        self.reads_options = []
        self.app_count_cache = 0

    @classmethod
    def register_helper(cls, klass, type, name):
        cls.specific_helpers[(type, name)] = klass

    @classmethod
    def find_helper(cls, criterion):
        helper = cls.specific_helpers.get(
            (criterion.type, criterion.name),
            cls
        )(criterion)
        return helper

    def options(self, spec, apps):
        return [spec.option]

    def app_count(self, apps, option_name):
        if self.app_count_cache == 0:
            self.app_count_cache = apps.count()
        return self.app_count_cache

    def remaining_capacity(self,
                           assignment_counts,
                           option_spec,
                           option,
                           judge_to_capacity_cache):
        result = 0

        for judge in judge_to_capacity_cache:
            if self.judge_matches_option(judge, option):
                result += max(0, judge['capacity'] - assignment_counts.get(
                    judge['judge_id'], 0))
        return result

    @classmethod
    def clone_criteria(cls, source_judging_round_id, target_judging_round_id):
        '''Clone criteria and options from one judging round to another.
        Used by CloneCriteriaView
        '''
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
    def clone_criterion(cls, criterion, target_judging_round_id):
        clone = cls.model.objects.create(
            judging_round_id=target_judging_round_id,
            type=criterion.type,
            name=criterion.name)
        return criterion.pk, clone.pk

    @classmethod
    def fields(cls):
        return ALL_FIELDS

    def option_for_field(self, field):
        return ""

    def field_matches_option(self, field, option):
        return True

    def judge_matches_option(self, judge_data, option):
        return True

    def app_state_analysis_fields(self):
        return self.analysis_fields()

    def analysis_annotate_fields(self):
        return {}

    def get_app_state_criteria_annotate_fields(self):
        return self.analysis_annotate_fields()

    def analysis_fields(self):
        return []

    def analysis_tally(self, app_id, db_value, cache, **kwargs):

        if not self.reads_options:
            options = self.subject.criterionoptionspec_set.values_list(
                'option', flat=True).distinct()
            for option in options:
                self.reads_options.append(option)

        for option in self.reads_options:
            reads_value = cache[app_id]["reads"].get(option)
            cache[app_id]["reads"][option] = (
                1 if reads_value is None else reads_value + 1)
