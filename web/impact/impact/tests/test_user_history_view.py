# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json

from django.urls import reverse
from django.utils import timezone
from jsonschema import Draft4Validator

from accelerator.models import UserRole
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import (
    JudgingRoundFactory,
    NewsletterReceiptFactory,
    ProgramCycleFactory,
    ProgramRoleGrantFactory,
    StartupTeamMemberFactory,
    UserFactory,
)
from impact.tests.utils import (
    assert_fields,
    days_from_now,
    find_events,
)
from impact.v1.events import (
    UserBecameConfirmedJudgeEvent,
    UserBecameConfirmedMentorEvent,
    UserBecameDesiredJudgeEvent,
    UserBecameDesiredMentorEvent,
    UserBecameFinalistEvent,
    UserCreatedEvent,
    UserJoinedStartupEvent,
    UserReceivedNewsletterEvent,
)
from impact.v1.views import UserHistoryView


class TestUserHistoryView(APITestCase):
    def test_user_created(self):
        user = UserFactory(date_joined=timezone.now())
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[user.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(user.date_joined, events[0]["datetime"])

    def test_user_joined_startup(self):
        stm = StartupTeamMemberFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[stm.user.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserJoinedStartupEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(stm.created_at, events[0]["datetime"])
            startup = stm.startup
            startup_str = UserJoinedStartupEvent.DESCRIPTION_FORMAT.format(
                name=startup.name,
                id=startup.organization.id)
            self.assertEqual(startup_str, events[0]["description"])

    def test_user_joined_startup_no_created_at(self):
        join_date = days_from_now(-10)
        stm = StartupTeamMemberFactory(user__date_joined=join_date)
        stm.created_at = None
        stm.save()
        next_created_at = days_from_now(-1)
        next_stm = StartupTeamMemberFactory()
        next_stm.created_at = next_created_at
        next_stm.save()
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[stm.user.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserJoinedStartupEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(join_date, events[0]["datetime"])
            self.assertEqual(next_created_at, events[0]["latest_datetime"])

    def test_user_became_finalist(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.FINALIST)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prg.created_at, events[0]["datetime"])
            self.assertEqual(prg.program_role.program.name,
                             events[0]["program"])
            self.assertEqual(prg.program_role.program.cycle.name,
                             events[0]["cycle"])

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
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
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
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(deadline, events[0]["datetime"])

    def test_user_became_confirmed_judge(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.PROGRAM_ROLE_FORMAT
            self.assertEqual(format_string.format(
                    role_name=UserBecameConfirmedJudgeEvent.ROLE_NAME,
                    name=prg.program_role.name,
                    id=prg.program_role.id),
                    events[0]["description"])

    def test_user_became_confirmed_judge_with_missing_label(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE,
            program_role__user_label=None)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.PROGRAM_ROLE_FORMAT
            self.assertEqual(format_string.format(
                role_name=UserBecameConfirmedJudgeEvent.ROLE_NAME,
                name=prg.program_role.name,
                id=prg.program_role.id),
                events[0]["description"])

    def test_user_became_confirmed_judge_with_judging_round(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE)
        jr = JudgingRoundFactory(
            confirmed_judge_label=prg.program_role.user_label)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.JUDGING_ROUND_FORMAT
            self.assertEqual(format_string.format(
                role_name=UserBecameConfirmedJudgeEvent.ROLE_NAME,
                name=jr.short_name(),
                id=jr.id),
                events[0]["description"])
            self.assertEqual(jr.id, events[0]["judging_round_id"])
            self.assertEqual(jr.short_name(), events[0]["judging_round_name"])

    def test_user_became_confirmed_judge_with_cycle_based_judging_round(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.JUDGE)
        jr = JudgingRoundFactory(
            confirmed_judge_label=prg.program_role.user_label,
            cycle_based_round=True)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameConfirmedJudgeEvent.JUDGING_ROUND_FORMAT
            self.assertEqual(format_string.format(
                role_name=UserBecameConfirmedJudgeEvent.ROLE_NAME,
                name=jr.short_name(),
                id=jr.id),
                events[0]["description"])

    def test_user_became_desired_judge(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.DESIRED_JUDGE)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameDesiredJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameDesiredJudgeEvent.PROGRAM_ROLE_FORMAT
            self.assertEqual(format_string.format(
                role_name=UserBecameDesiredJudgeEvent.ROLE_NAME,
                name=prg.program_role.name,
                id=prg.program_role.id),
                events[0]["description"])

    def test_user_became_desired_judge_with_missing_label(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.DESIRED_JUDGE,
            program_role__user_label=None)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameDesiredJudgeEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            format_string = UserBecameDesiredJudgeEvent.PROGRAM_ROLE_FORMAT
            self.assertEqual(format_string.format(
                role_name=UserBecameDesiredJudgeEvent.ROLE_NAME,
                name=prg.program_role.name,
                id=prg.program_role.id),
                events[0]["description"])

    def test_user_became_confirmed_mentor(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.MENTOR)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameConfirmedMentorEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prg.created_at, events[0]["datetime"])

    def test_user_became_desired_mentor(self):
        prg = ProgramRoleGrantFactory(
            program_role__user_role__name=UserRole.DESIRED_MENTOR)
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[prg.person.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserBecameDesiredMentorEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prg.created_at, events[0]["datetime"])

    def test_user_received_newsletter(self):
        receipt = NewsletterReceiptFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name,
                          args=[receipt.recipient.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 UserReceivedNewsletterEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(receipt.created_at, events[0]["datetime"])
            self.assertEqual(receipt.newsletter.name,
                             events[0]["newsletter_name"])
            self.assertEqual(receipt.newsletter.from_addr,
                             events[0]["newsletter_from_address"])

    def test_options(self):
        user = UserFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[user.id])
            response = self.client.options(url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(UserHistoryView.fields().keys(), get_options)

    def test_options_against_get(self):
        user = UserFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(UserHistoryView.view_name, args=[user.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
