# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# TODO: Coverage, tests that make reasonable selections
# Need to account for completed feedback
# Need to account for existing assignments
# Need to instrument other CriterionHelpers

from collections import namedtuple
from django.urls import reverse

from accelerator.models import Application
from accelerator.tests.factories import (
    ExpertFactory,
    JudgeRoundCommitmentFactory,
    ProgramFactory,
)
from accelerator.tests.contexts import AnalyzeJudgingContext
from impact.tests.api_test_case import APITestCase
from impact.v1.views import (
    ALREADY_ASSIGNED_ERROR,
    AllocateApplicationsView,
    JUDGING_ROUND_INACTIVE_ERROR,
    NO_APP_LEFT_FOR_JUDGE,
    NO_DATA_FOR_JUDGE,
)


JudgeWithPanel = namedtuple('JudgeWithPanel', ['option', 'judge', 'panel'])


class TestAllocateApplicationsView(APITestCase):
    def test_get(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        judge = context.add_judge()
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 200

    def test_get_judging_round_inactive(self):
        context = AnalyzeJudgingContext(is_active=False)
        judging_round = context.judging_round
        judge = context.add_judge()
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 403
            assert [JUDGING_ROUND_INACTIVE_ERROR.format(judging_round.id)
                    in response.data]

    def test_get_already_assigned(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        judge = context.add_judge()
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 200
            count = len(response.data)
            response = self.client.get(url)
            assert response.status_code == 403
            assert [ALREADY_ASSIGNED_ERROR.format(judge=judge.email,
                                                  count=count)
                    in response.data]

    def test_get_no_app_for_judge(self):
        context = AnalyzeJudgingContext()
        for app in context.applications:
            if not app.judgeapplicationfeedback_set.filter(
                    judge=context.judge).exists():
                context.add_feedback(application=app,
                                     judge=context.judge,
                                     panel=context.panel)
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[context.judging_round.id, context.judge.id])
            response = self.client.get(url)
            assert response.status_code == 403
            assert [NO_APP_LEFT_FOR_JUDGE.format(context.judge.email)
                    in response.data]

    def test_get_adds_capacity_and_quota(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        commitment = JudgeRoundCommitmentFactory(judge=context.judge,
                                                 judging_round=judging_round,
                                                 capacity=0,
                                                 current_quota=0)
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, context.judge.id])
            response = self.client.get(url)
            assert response.status_code == 200
            commitment.refresh_from_db()
            assert commitment.capacity > 0
            assert commitment.current_quota > 0

    def test_get_for_unknown_judge_fails(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        judge = ExpertFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 403
            assert [
                NO_DATA_FOR_JUDGE.format(
                    judging_round=context.judging_round,
                    judge=context.judge.email) in response.data
            ]

    def test_get_by_judge_succeeds(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        judge = context.add_judge()
        judge.set_password("password")
        judge.save()
        with self.login(email=judge.email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            response = self.client.get(url)
            assert response.status_code == 200

    def test_get_by_another_expert_fails(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        judge = context.judge
        judge.set_password("password")
        judge.save()
        with self.login(email=judge.email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, ExpertFactory().id])
            response = self.client.get(url)
            assert response.status_code == 403

    def test_get_full_panel(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        panel_size = context.scenario.panel_size
        context.add_applications(panel_size * 2)
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, context.judge.id])
            response = self.client.get(url)
            assert len(response.data) == panel_size

    def test_get_gender_filter(self):
        self.assert_judge_feature_filter("gender",
                                         ["f", "m"],
                                         "profile__gender")

    def test_get_role_filter(self):
        self.assert_judge_feature_filter("role",
                                         ["Executive", "Lawyer", "Investor"],
                                         "profile__expert_category__name")

    def assert_judge_feature_filter(self, name, options, field):
        context = AnalyzeJudgingContext(type="judge",
                                        name=name,
                                        read_count=1,
                                        options=options)
        judge_with_panels = [_judge_with_panel(context, field, option)
                             for option in options]
        count = len(options)
        context.add_applications(context.scenario.panel_size * count)
        for counter, app in enumerate(context.applications):
            (option, judge, panel) = judge_with_panels[counter % count]
            context.add_feedback(application=app, judge=judge, panel=panel)
        example = judge_with_panels[0]
        new_judge = ExpertFactory(**{field: example.option})
        context.add_judge(assigned=False,
                          complete=False,
                          judge=new_judge)
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[context.judging_round.id, new_judge.id])
            self.client.get(url)
            example_apps = example.judge.judgepanelassignment_set.values_list(
                "panel__applicationpanelassignment__application_id", flat=True)
            new_judge_apps = new_judge.judgepanelassignment_set.values_list(
                "panel__applicationpanelassignment__application_id", flat=True)
            assert set(example_apps).intersection(new_judge_apps) == set()

    def test_get_industry_filter(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="industry",
                                        read_count=1)
        options = [app.startup.primary_industry
                   for app in context.applications]
        count = len(options)
        assert(count > 1)
        field = "startup__primary_industry"
        context.add_applications(context.scenario.panel_size * count,
                                 field=field,
                                 options=options)
        judge_option = options[0]
        judge = ExpertFactory(profile__primary_industry=judge_option)
        context.add_judge(assigned=False,
                          complete=False,
                          judge=judge)
        apps = Application.objects.filter(
            **{field: judge_option}).values_list("id", flat=True)
        self.assert_matching_allocation(context.judging_round, judge, apps)

    # TODO: Test that uses a child industry

    def test_get_program_filter(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="program",
                                        read_count=1)
        count = 4
        options = ProgramFactory.create_batch(count, cycle=context.cycle)
        context.add_applications(context.scenario.panel_size * count,
                                 programs=options)
        judge_option = options[0].program_family
        judge = ExpertFactory(profile__home_program_family=judge_option)
        context.add_judge(assigned=False,
                          complete=False,
                          judge=judge)
        field = "startup__startupprograminterest__program__program_family"
        apps = Application.objects.filter(
            **{field: judge_option}).values_list("id", flat=True)
        self.assert_matching_allocation(context.judging_round, judge, apps)

    # TODO: Test that has a startup with interest in more than one program

    def assert_matching_allocation(self, judging_round, judge, apps):
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, judge.id])
            self.client.get(url)
            judge_apps = set(
                judge.judgepanelassignment_set.values_list(
                    "panel__applicationpanelassignment__application_id",
                    flat=True))
            matches = set(apps).intersection(judge_apps)
            assert matches == judge_apps


def _judge_with_panel(context, field, option):
    panel = context.add_panel()
    judge = ExpertFactory(**{field: option})
    context.add_judge(complete=False, judge=judge, panel=panel)
    return JudgeWithPanel(option, judge, panel)
