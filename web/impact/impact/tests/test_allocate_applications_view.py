# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from accelerator.tests.factories import (
    ExpertFactory,
    JudgeApplicationFeedbackFactory,
    JudgeRoundCommitmentFactory,
)
from accelerator.tests.contexts import JudgeFeedbackContext
from impact.tests.api_test_case import APITestCase
from impact.v1.views import (
    ALREADY_ASSIGNED_ERROR,
    AllocateApplicationsView,
    JUDGING_ROUND_INACTIVE_ERROR,
    NO_APP_LEFT_FOR_JUDGE,
)


class TestAllocateApplicationsView(APITestCase):
    def test_get(self):
        context = JudgeFeedbackContext()
        judging_round = context.judging_round
        judge_id = ExpertFactory().id
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge_id])
            response = self.client.get(url)
            assert response.status_code == 200

    def test_get_judging_round_inactive(self):
        context = JudgeFeedbackContext(is_active=False)
        judging_round = context.judging_round
        judge_id = ExpertFactory().id
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge_id])
            response = self.client.get(url)
            assert response.status_code == 403
            assert [JUDGING_ROUND_INACTIVE_ERROR.format(judging_round.id)
                    in response.data]

    def test_get_already_assigned(self):
        context = JudgeFeedbackContext()
        judging_round = context.judging_round
        judge_id = ExpertFactory().id
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge_id])
            response = self.client.get(url)
            assert response.status_code == 200
            count = len(response.data)
            response = self.client.get(url)
            assert response.status_code == 403
            assert [ALREADY_ASSIGNED_ERROR.format(judge=context.judge.email,
                                                  count=count)
                    in response.data]

    def test_get_no_app_for_judge(self):
        context = JudgeFeedbackContext()
        judge = ExpertFactory()
        for app in context.applications:
            JudgeApplicationFeedbackFactory(panel=context.panel,
                                            judge=judge,
                                            application=app)
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[context.judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 403
            assert [NO_APP_LEFT_FOR_JUDGE.format(context.judge.email)
                    in response.data]

    def test_get_adds_capacity_and_quota(self):
        context = JudgeFeedbackContext()
        judging_round = context.judging_round
        judge = ExpertFactory()
        commitment = JudgeRoundCommitmentFactory(judge=judge,
                                                 judging_round=judging_round,
                                                 capacity=0,
                                                 current_quota=0)
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 200
            commitment.refresh_from_db()
            assert commitment.capacity > 0
            assert commitment.current_quota > 0

    def test_get_by_judge_succeeds(self):
        context = JudgeFeedbackContext()
        judging_round = context.judging_round
        judge = ExpertFactory()
        judge.set_password("password")
        judge.save()
        with self.login(email=judge.email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 200

    def test_get_by_another_expert_fails(self):
        context = JudgeFeedbackContext()
        judging_round = context.judging_round
        judge = ExpertFactory()
        judge.set_password("password")
        judge.save()
        with self.login(email=judge.email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, ExpertFactory().id])
            response = self.client.get(url)
            assert response.status_code == 403
