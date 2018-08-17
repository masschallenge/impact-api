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
    JudgingRound,
)
from accelerator.tests.factories import (
    CriterionOptionSpecFactory,
    JudgingRoundFactory,
)


class TestCloneCriteriaView(APITestCase):
    def test_successful_clone(self):
        option_spec = CriterionOptionSpecFactory()
        old_round = option_spec.criterion.judging_round
        new_round = JudgingRoundFactory()
        url = reverse(CloneCriteriaView.view_name)
        data = {SOURCE_JUDGING_ROUND_KEY: old_round.pk,
                TARGET_JUDGING_ROUND_KEY: new_round.pk}
        with self.login(email=self.basic_user().email):
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
        with self.login(email=self.basic_user().email):
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
        round_ids = [jr.pk for jr in JudgingRoundFactory.create_batch(2)]
        data = {SOURCE_JUDGING_ROUND_KEY: round_ids[0],
                TARGET_JUDGING_ROUND_KEY: round_ids[1]}
        JudgingRound.objects.filter(pk__in=round_ids).delete()
        url = reverse(CloneCriteriaView.view_name)

        with self.login(email=self.basic_user().email):
            response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401)
