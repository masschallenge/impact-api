# MIT License
# Copyright (c) 2018 MassChallenge, Inc.

from datetime import (
    datetime,
    timedelta,
    )
from pytz import utc
from collections import namedtuple
from itertools import chain
from django.urls import reverse

from mc.models import (
    Application,
    JUDGING_FEEDBACK_STATUS_CONFLICT,
    JUDGING_STATUS_CONFLICT,
    StartupProgramInterest,
)
from accelerator.tests.factories import (
    AllocatorFactory,
    ApplicationPanelAssignmentFactory,
    CriterionOptionSpecFactory,
    ExpertFactory,
    IndustryFactory,
    JudgeApplicationFeedbackFactory,
    JudgePanelAssignmentFactory,
    ProgramFactory,
    StartupProgramInterestFactory,
)
from accelerator.tests.contexts import (
    AnalyzeJudgingContext,
    JudgeFeedbackContext,
)
from .api_test_case import APITestCase
from ..v1.views import (
    ALREADY_ASSIGNED_ERROR,
    AllocateApplicationsView,
    JUDGING_ROUND_INACTIVE_ERROR,
    NO_APP_LEFT_FOR_JUDGE,
    NO_DATA_FOR_JUDGE,
)


JudgeWithPanel = namedtuple('JudgeWithPanel', ['option', 'judge', 'panel'])


class TestAllocateApplicationsView(APITestCase):
    def _url(self, judging_round_id, judge_id):
        return reverse(AllocateApplicationsView.view_name,
                       args=[judging_round_id, judge_id])

    def test_get(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        judge = context.add_judge()
        with self.login(email=self.basic_user().email):

            response = self.client.get(self._url(judging_round.id,
                                                 judge.id))
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

    def test_allocator_respects_completed_assignments(self):
        context = AnalyzeJudgingContext()
        AllocatorFactory(judging_round=context.judging_round,
                         scenario=context.scenario)
        context.add_applications(20)
        panel = context.add_panel()
        for app in context.applications[-10:]:
            ApplicationPanelAssignmentFactory(
                application=app,
                panel=panel,
                scenario=context.scenario)
        context.add_judge(assigned=True,
                          complete=True,
                          panel=panel)
        new_judge = context.add_judge(assigned=False,
                                      complete=False)
        new_judge.set_password("password")
        new_judge.save()
        with self.login(email=new_judge.email):
            response = self.client.get(self._url(context.judging_round.id,
                                                 new_judge.id))
        assignments = response.json()
        assigned_ids = [app.id for app in context.applications[-10:]]
        reassigned_apps = set(assignments).intersection(assigned_ids)
        assert 0 == len(reassigned_apps)

    def test_allocator_assignment_discount_times_out(self):
        context = JudgeFeedbackContext(complete=False)

        CriterionOptionSpecFactory(
            criterion__judging_round=context.judging_round,
            criterion__type="reads",
            criterion__name="reads",
            option="",
            count=4,
            weight=1)
        AllocatorFactory(judging_round=context.judging_round,
                         scenario=context.scenario)
        old_assigned_apps = context.add_applications(10)
        new_assigned_apps = context.add_applications(10)
        old_panel = context.add_panel()
        new_panel = context.panel
        now = utc.localize(datetime.utcnow())
        six_days_ago = now - timedelta(6)
        for app in old_assigned_apps:
            apa = ApplicationPanelAssignmentFactory(
                application=app,
                panel=old_panel,
                scenario=context.scenario)
            apa.created_at = six_days_ago
            apa.save()
        jpa = JudgePanelAssignmentFactory(
            panel=old_panel,
            judge=context.judge,
            scenario=context.scenario)
        jpa.created_at = six_days_ago
        jpa.save()
        for app in new_assigned_apps:
            ApplicationPanelAssignmentFactory(
                application=app,
                panel=new_panel,
                scenario=context.scenario)
        new_judge = context.add_judge(assigned=False,
                                      complete=False)
        new_judge.set_password("password")
        new_judge.save()
        with self.login(email=new_judge.email):
            response = self.client.get(self._url(context.judging_round.id,
                                                 new_judge.id))
        assignments = response.json()
        assigned_ids = [app.id for app in old_assigned_apps]
        reassigned_apps = set(assignments).intersection(assigned_ids)
        self.assertEqual(10, len(reassigned_apps))

    def test_allocator_does_not_reassign_conflicted_apps_to_same_judge(self):
        context = AnalyzeJudgingContext()
        AllocatorFactory(judging_round=context.judging_round,
                         scenario=context.scenario)
        context.add_applications(20)
        panel = context.add_panel()
        for app in context.applications[-10:]:
            ApplicationPanelAssignmentFactory(
                application=app,
                panel=panel,
                scenario=context.scenario)
        judge = context.add_judge(assigned=True,
                                  complete=True,
                                  panel=panel)
        for app in context.applications[-10:]:
            JudgeApplicationFeedbackFactory(
                application=app,
                form_type=context.judging_round.judging_form,
                judge=judge,
                panel=panel,
                judging_status=JUDGING_STATUS_CONFLICT,
                feedback_status=JUDGING_FEEDBACK_STATUS_CONFLICT
            )
        judge.set_password("password")
        judge.save()
        with self.login(email=judge.email):
            response = self.client.get(self._url(context.judging_round.id,
                                                 judge.id))
        assignments = response.json()
        assigned_ids = [app.id for app in context.applications[-10:]]
        reassigned_apps = set(assignments).intersection(assigned_ids)
        assert 0 == len(reassigned_apps)

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

    def test_get_industry_filter_with_child_industry(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="industry",
                                        read_count=1)
        child_industry = IndustryFactory()
        child_industry.parent = IndustryFactory()
        child_industry.save()
        field = "startup__primary_industry"
        context.add_applications(context.scenario.panel_size,
                                 field=field,
                                 options=[child_industry])
        parent_industry = child_industry.parent
        judge = ExpertFactory(profile__primary_industry=parent_industry)
        context.add_judge(assigned=False,
                          complete=False,
                          judge=judge)
        apps = Application.objects.filter(
            **{field: child_industry}).values_list("id", flat=True)
        self.assert_matching_allocation(context.judging_round, judge, apps)

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

    def test_get_program_filter_multiple_startup_interests(self):
        context = AnalyzeJudgingContext(type="matching",
                                        name="program",
                                        read_count=1)
        count = 4
        options = ProgramFactory.create_batch(count, cycle=context.cycle)
        panel_size = context.scenario.panel_size
        context.add_applications(panel_size * count,
                                 programs=options)
        judge_option = options[0].program_family
        judge = ExpertFactory(profile__home_program_family=judge_option)
        context.add_judge(assigned=False,
                          complete=False,
                          judge=judge)
        programs = chain(options[1:], options * panel_size)
        for app, program in zip(context.applications, programs):
            StartupProgramInterestFactory(startup=app.startup,
                                          program=program,
                                          order=2)
        spis = StartupProgramInterest.objects.filter(order=1,
                                                     program__in=options)
        app_filter = {"startup__startupprograminterest__in": spis}
        apps = Application.objects.filter(**app_filter).values_list("id",
                                                                    flat=True)
        self.assert_matching_allocation(context.judging_round, judge, apps)

    def test_commitment_quota_none_is_tolerated(self):
        context = AnalyzeJudgingContext()
        judging_round = context.judging_round
        commitment = context.judges[0].judgeroundcommitment_set.first()
        commitment.current_quota = None
        commitment.save()
        with self.login(email=self.basic_user().email):
            url = reverse(AllocateApplicationsView.view_name,
                          args=[judging_round.id, context.judge.id])
            # No error == success
            self.client.get(url)

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
