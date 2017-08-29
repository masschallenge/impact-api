# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.models import UserRole
from impact.tests.factories import (
    JudgingRoundFactory,
    ProgramCycleFactory,
    ProgramRoleGrantFactory,
    StartupTeamMemberFactory,
    UserFactory,
)
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import (
    days_from_now,
    find_events,
)

from impact.v1.events import (
    UserBecameConfirmedJudgeEvent,
    UserBecameConfirmedMentorEvent,
    UserBecameFinalistEvent,
    UserCreatedEvent,
    UserJoinedStartupEvent,
)


class TestUserHistoryView(APITestCase):
    def test_user_created(self):
        user = UserFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[user.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(user.date_joined, events[0]["datetime"])

    def test_user_joined_startup(self):
        stm = StartupTeamMemberFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[stm.user.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserJoinedStartupEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(stm.created_at, events[0]["datetime"])

    def test_user_joined_startup_no_created_at(self):
        join_date = days_from_now(-10)
        stm = StartupTeamMemberFactory(user__date_joined=join_date)
        stm.created_at = None
        stm.save()
        next_created_at = days_from_now(-1)
        next_stm = StartupTeamMemberFactory()
        next_stm.created_at = next_created_at
        next_stm.save()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[stm.user.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserJoinedStartupEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(join_date, events[0]["datetime"])
            self.assertEqual(next_created_at, events[0]["latest_datetime"])

    def test_user_became_finalist(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.FINALIST)
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prg.created_at, events[0]["datetime"])

    def test_user_became_finalist_no_created_at_new_user(self):
        deadline = days_from_now(-4)
        cycle = ProgramCycleFactory(application_final_deadline_date=deadline)
        user_date = days_from_now(-2)
        user = UserFactory(date_joined=user_date)
        prg = ProgramRoleGrantFactory(
            person=user,
            program_role__program__cycle=cycle,
            program_role__user_role__name=UserRole.FINALIST)
        prg.created_at = None
        prg.save()
        next_prg_date = days_from_now(-1)
        next_prg = ProgramRoleGrantFactory()
        next_prg.created_at = next_prg_date
        next_prg.save()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(user_date, events[0]["datetime"])
            self.assertEqual(next_prg_date, events[0]["latest_datetime"])

    def test_user_became_finalist_no_created_at_old_user(self):
        user_date = days_from_now(-4)
        user = UserFactory(date_joined=user_date)
        deadline = days_from_now(-2)
        cycle = ProgramCycleFactory(application_final_deadline_date=deadline)
        prg = ProgramRoleGrantFactory(
            person=user,
            program_role__program__cycle=cycle,
            program_role__user_role__name=UserRole.FINALIST)
        prg.created_at = None
        prg.save()
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(deadline, events[0]["datetime"])

    def test_user_became_confirmed_judge(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE)
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.PROGRAM_ROLE_FORMAT
            self.assertEqual(format_string.format(name=prg.program_role.name,
                                                  id=prg.program_role.id),
                             events[0]["description"])

    def test_user_became_confirmed_judge_with_judging_round(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE)
        jr = JudgingRoundFactory(
            confirmed_judge_label=prg.program_role.user_label)
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.JUDGING_ROUND_FORMAT
            self.assertEqual(format_string.format(name=jr.short_name(),
                                                  id=jr.id),
                             events[0]["description"])

    def test_user_became_confirmed_judge_with_cycle_based_judging_round(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE)
        jr = JudgingRoundFactory(
            confirmed_judge_label=prg.program_role.user_label,
            cycle_based_round=True)
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.JUDGING_ROUND_FORMAT
            self.assertEqual(format_string.format(name=jr.short_name(),
                                                  id=jr.id),
                             events[0]["description"])

    def test_user_became_confirmed_mentor(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.MENTOR)
        with self.login(username=self.basic_user().username):
            url = reverse("user_history", args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedMentorEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prg.created_at, events[0]["datetime"])
