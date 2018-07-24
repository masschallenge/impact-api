# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.tests.api_test_case import APITestCase
from impact.v1.views import CloneCriteriaView
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
        url = reverse(CloneCriteriaView.view_name,
                      args=[old_round.pk, new_round.pk])
        with self.login(email=self.basic_user().email):
            response=self.client.get(url)
        assert CriterionOptionSpec.objects.filter(
            option=option_spec.option,
            weight=option_spec.weight,
            count=option_spec.count,
            criterion__judging_round=new_round).exists()

    def test_judging_rounds_do_not_exist(self):
        round_ids = [jr.pk for jr in JudgingRoundFactory.create_batch(2)]
        JudgingRound.objects.filter(pk__in=round_ids).delete()
        url = reverse(CloneCriteriaView.view_name,
                      args=round_ids)
        
        with self.login(email=self.basic_user().email):
            response=self.client.get(url)
        self.assertEqual(response.status_code, 401)
    
