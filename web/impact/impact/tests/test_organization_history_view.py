# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from mc.models import (
    SUBMITTED_APP_STATUS,
    StartupRole,
)
from .factories import (
    ApplicationFactory,
    OrganizationFactory,
    PartnerFactory,
    ProgramCycleFactory,
    ProgramFactory,
    StartupFactory,
    StartupProgramInterestFactory,
    StartupStatusFactory,
)

from .api_test_case import APITestCase
from .utils import (
    assert_fields,
    days_from_now,
    find_events,
)
from ..utils import DAWN_OF_TIME
from ..v1.events import (
    OrganizationBecameEntrantEvent,
    OrganizationBecameFinalistEvent,
    OrganizationBecameWinnerEvent,
    OrganizationCreatedEvent,
)
from ..v1.views import OrganizationHistoryView


class TestOrganizationHistoryView(APITestCase):
    def test_startup_created(self):
        startup = StartupFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(startup.created_at, events[0]["datetime"])

    def test_startup_created_with_created_datetime(self):
        startup = StartupFactory()
        startup.created_at = None
        startup.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(startup.created_datetime, events[0]["datetime"])

    def test_startup_created_no_created_datetime(self):
        startup = StartupFactory(created_datetime=None)
        startup.created_at = None
        startup.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(DAWN_OF_TIME, events[0]["datetime"])

    def test_startup_created_using_other_startups(self):
        prev_created_datetime = days_from_now(-10)
        StartupFactory(created_datetime=prev_created_datetime)
        startup = StartupFactory(created_datetime=None)
        startup.created_at = None
        startup.save()
        next_created_datetime = days_from_now(-2)
        StartupFactory(created_datetime=next_created_datetime)
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prev_created_datetime, events[0]["datetime"])
            self.assertEqual(next_created_datetime,
                             events[0]["latest_datetime"])

    def test_partner_created(self):
        partner = PartnerFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[partner.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(partner.created_at, events[0]["datetime"])

    def test_partner_created_no_created_at(self):
        partner = PartnerFactory()
        partner.created_at = None
        partner.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[partner.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(DAWN_OF_TIME, events[0]["datetime"])

    def test_partner_created_using_later_partner(self):
        prev_partner = PartnerFactory()
        prev_created_at = days_from_now(-10)
        prev_partner.created_at = prev_created_at
        prev_partner.save()
        partner = PartnerFactory()
        partner.created_at = None
        partner.save()
        next_partner = PartnerFactory()
        next_created_at = days_from_now(-2)
        next_partner.created_at = next_created_at
        next_partner.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[partner.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prev_created_at, events[0]["datetime"])
            self.assertEqual(next_created_at, events[0]["latest_datetime"])

    def test_organization_created(self):
        org = OrganizationFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[org.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(org.created_at, events[0]["datetime"])

    def test_startup_became_entrant(self):
        program = ProgramFactory()
        cycle = program.cycle
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            cycle=cycle)
        startup = application.startup
        StartupProgramInterestFactory(startup=startup,
                                      program=program,
                                      applying=True)
        startup_status = StartupStatusFactory(
            startup=startup,
            program_startup_status__program=program,
            program_startup_status__startup_role__name=StartupRole.ENTRANT)
        startup_status.created_at = days_from_now(-1)
        startup_status.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(cycle.name in events[0]["description"])
            self.assertEqual(startup_status.created_at, events[0]["datetime"])
            self.assertEqual(program.id, events[0]["program_id"])
            self.assertEqual(program.name, events[0]["program"])
            self.assertEqual(1, events[0]["program_preference"])

    def test_startup_became_entrant_for_multiple_programs(self):
        cycle = ProgramCycleFactory()
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            cycle=cycle)
        startup = application.startup
        INTEREST_COUNT = 2
        StartupProgramInterestFactory.create_batch(INTEREST_COUNT,
                                                   startup=startup,
                                                   program__cycle=cycle,
                                                   applying=True)
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(INTEREST_COUNT, len(events))

    def test_startup_became_entrant_no_startup_status(self):
        program = ProgramFactory()
        cycle = program.cycle
        submission_datetime = days_from_now(-2)
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            submission_datetime=submission_datetime,
            cycle=cycle)
        startup = application.startup
        StartupProgramInterestFactory(startup=startup,
                                      program=program,
                                      applying=True)
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(cycle.name in events[0]["description"])
            self.assertEqual(submission_datetime, events[0]["datetime"])

    def test_startup_became_entrant_no_submission_datetime(self):
        cycle_deadline = days_from_now(-1)
        cycle = ProgramCycleFactory(
            application_final_deadline_date=cycle_deadline)
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            cycle=cycle,
            submission_datetime=None)
        startup = application.startup
        StartupProgramInterestFactory(startup=startup,
                                      program__cycle=cycle,
                                      applying=True)
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(cycle_deadline,
                             events[0]["datetime"])

    def test_startup_became_finalist(self):
        startup = StartupFactory()
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.FINALIST,
            startup=startup)
        program = startup_status.program_startup_status.program
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(program.name in events[0]["description"])
            self.assertEqual(program.name, events[0]["program"])
            self.assertEqual(program.id, events[0]["program_id"])
            self.assertEqual(program.cycle.name, events[0]["cycle"])
            self.assertEqual(program.cycle.id, events[0]["cycle_id"])

    def test_startup_became_finalist_no_created_at(self):
        startup = StartupFactory()
        start_date = days_from_now(10)
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.FINALIST,
            program_startup_status__program__start_date=start_date,
            startup=startup)
        startup_status.created_at = None
        startup_status.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(start_date, events[0]["datetime"])

    def test_startup_became_winner(self):
        startup = StartupFactory()
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.GOLD_WINNER,
            startup=startup)
        role = startup_status.program_startup_status.startup_role
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameWinnerEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(role.name, events[0]["winner_level"])

    def test_startup_became_winner_no_created_at(self):
        startup = StartupFactory()
        end_date = days_from_now(-10)
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.GOLD_WINNER,
            program_startup_status__program__end_date=end_date,
            startup=startup)
        startup_status.created_at = None
        startup_status.save()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameWinnerEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(end_date, events[0]["datetime"])

    def test_options(self):
        startup = StartupFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name, args=[startup.id])
            response = self.client.options(url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(OrganizationHistoryView.fields().keys(), get_options)

    def test_options_against_get(self):
        startup = StartupFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(OrganizationHistoryView.view_name, args=[startup.id])

            options_response = self.client.options(url)
            get_response = self.client.get(url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))
