# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.api_test_case import APITestCase
from impact.v1.views import (
    CloneCriteriaView,
    SOURCE_JUDGING_ROUND_KEY,
    TARGET_JUDGING_ROUND_KEY,
)
from accelerator.models import (
    CriterionOptionSpec,
)
from accelerator.tests.factories import (
    CriterionOptionSpecFactory,
    JudgingRoundFactory,
)
from impact.tests.utils import assert_fields

class TestCloneCriteriaView(APITestCase):
    def test_global_operations_manager_permission_required(self):
        option_spec = CriterionOptionSpecFactory()
        old_round = option_spec.criterion.judging_round
        new_round = JudgingRoundFactory()
        url = reverse(CloneCriteriaView.view_name)
        data = {SOURCE_JUDGING_ROUND_KEY: old_round.pk,
                TARGET_JUDGING_ROUND_KEY: new_round.pk}
        program_family = new_round.program.program_family
        email = self.basic_user().email
        with self.login(email=email):
            response = self.client.post(url, data=data)
        assert response.status_code == 403

    
    def test_successful_clone(self):
        option_spec = CriterionOptionSpecFactory()
        old_round = option_spec.criterion.judging_round
        new_round = JudgingRoundFactory()
        url = reverse(CloneCriteriaView.view_name)
        data = {SOURCE_JUDGING_ROUND_KEY: old_round.pk,
                TARGET_JUDGING_ROUND_KEY: new_round.pk}
        program_family = new_round.program.program_family
        email = self.global_operations_manager(program_family).email
        with self.login(email=email):
            self.client.post(url, data=data)
        assert CriterionOptionSpec.objects.filter(
            option=option_spec.option,
            weight=option_spec.weight,
            count=option_spec.count,
            criterion__judging_round=new_round).exists()

    def test_existing_criteria_are_deleted_from_target_round(self):
        option_spec = CriterionOptionSpecFactory()
        old_round = option_spec.criterion.judging_round
        target_round_spec = CriterionOptionSpecFactory()
        target_round = target_round_spec.criterion.judging_round
        url = reverse(CloneCriteriaView.view_name)
        data = {SOURCE_JUDGING_ROUND_KEY: old_round.pk,
                TARGET_JUDGING_ROUND_KEY: target_round.pk}
        program_family = target_round.program.program_family
        email = self.global_operations_manager(program_family).email
        with self.login(email=email):
            self.client.post(url, data=data)
        self.assertEqual(
            CriterionOptionSpec.objects.filter(
                option=option_spec.option,
                weight=option_spec.weight,
                count=option_spec.count,
                criterion__judging_round=target_round).count(),
            1)
        self.assertFalse(CriterionOptionSpec.objects.filter(
            pk=target_round_spec.id).exists())

    def test_judging_rounds_do_not_exist(self):
        rounds = [jr for jr in JudgingRoundFactory.create_batch(2)]
        data = {SOURCE_JUDGING_ROUND_KEY: rounds[0].pk,
                TARGET_JUDGING_ROUND_KEY: rounds[1].pk}
        program_family = rounds[1].program.program_family
        [round.delete() for round in rounds]
        url = reverse(CloneCriteriaView.view_name)
        email = self.global_operations_manager(program_family).email
        with self.login(email=email):
            response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401)

    def test_options(self):
        program_family = JudgingRoundFactory().program.program_family
        email = self.global_operations_manager(program_family).email
        url = reverse(CloneCriteriaView.view_name)                    
        with self.login(email=email):
            response = self.client.options(url)
        results = response.data["actions"]["GET"]["properties"]["results"]
        get_options = results["item"]["properties"]
        assert_fields(CloneCriteriaView.fields().keys(), get_options)
