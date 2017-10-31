# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import json
from jsonschema import Draft4Validator

from django.urls import reverse

from impact.models import (
    SUBMITTED_APP_STATUS,
    StartupRole,
)
from impact.tests.factories import (
    ApplicationFactory,
    OrganizationFactory,
    PartnerFactory,
    ProgramCycleFactory,
    ProgramFactory,
    StartupFactory,
    StartupProgramInterestFactory,
    StartupStatusFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.tests.utils import (
    assert_fields,
    days_from_now,
    find_events,
)
from impact.utils import DAWN_OF_TIME
from impact.v1.events import (
    OrganizationBecameEntrantEvent,
    OrganizationBecameFinalistEvent,
    OrganizationCreatedEvent,
)
from impact.v1.views import OrganizationHistoryView


class TestOrganizationHistoryView(APITestCase):
    def test_startup_created(self):
        startup = StartupFactory()
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(cycle.name in events[0]["description"])
            self.assertEqual(startup_status.created_at, events[0]["datetime"])
            self.assertEqual([{"id": program.id,
                               "name": program.name,
                               "preference": 1}],
                             events[0]["programs"])

    def test_startup_became_entrant_no_startup_status(self):
        cycle = ProgramCycleFactory()
        submission_datetime = days_from_now(-2)
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            submission_datetime=submission_datetime,
            cycle=cycle)
        startup = application.startup
        with self.login(username=self.basic_user().username):
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
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(cycle_deadline,
                             events[0]["datetime"])

    def test_startup_became_entrant_no_final_deadline(self):
        cycle = ProgramCycleFactory(
            application_final_deadline_date=None)
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            cycle=cycle,
            submission_datetime=None)
        startup = application.startup
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(DAWN_OF_TIME,
                             events[0]["datetime"])

    def test_startup_became_entrant_no_final_deadline_with_other_cycles(self):
        prev_deadline = days_from_now(-10)
        ProgramCycleFactory(application_final_deadline_date=prev_deadline)
        cycle = ProgramCycleFactory(
            application_final_deadline_date=None)
        next_deadline = days_from_now(-5)
        ProgramCycleFactory(application_final_deadline_date=next_deadline)
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            cycle=cycle,
            submission_datetime=None)
        startup = application.startup
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prev_deadline,
                             events[0]["datetime"])
            self.assertEqual(next_deadline,
                             events[0]["latest_datetime"])

    def test_startup_became_finalist(self):
        startup = StartupFactory()
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.FINALIST,
            startup=startup)
        program = startup_status.program_startup_status.program
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(program.name in events[0]["description"])
            self.assertEqual(program.name, events[0]["program"])
            self.assertEqual(program.cycle.name, events[0]["cycle"])

    def test_startup_became_finalist_no_created_at(self):
        startup = StartupFactory()
        start_date = days_from_now(10)
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.FINALIST,
            program_startup_status__program__start_date=start_date,
            startup=startup)
        startup_status.created_at = None
        startup_status.save()
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name,
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["results"],
                                 OrganizationBecameFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(start_date, events[0]["datetime"])

    def test_options(self):
        startup = StartupFactory()
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name, args=[startup.id])
            response = self.client.options(url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(OrganizationHistoryView.fields().keys(), get_options)

    def test_options_against_get(self):
        startup = StartupFactory()
        with self.login(username=self.basic_user().username):
            url = reverse(OrganizationHistoryView.view_name, args=[startup.id])
            options_response = self.client.options(url)
            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            get_response = self.client.get(url)
            assert validator.is_valid(json.loads(get_response.content))
