# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

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
    StartupFactory,
    StartupStatusFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.tests.utils import (
    days_from_now,
    find_events,
)
from impact.utils import DAWN_OF_TIME
from impact.v1.events import (
    OrganizationBecomeEntrantEvent,
    OrganizationBecomeFinalistEvent,
    OrganizationCreatedEvent,
)


class TestOrganizationHistoryView(APITestCase):
    def test_startup_created(self):
        startup = StartupFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(startup.created_at, events[0]["datetime"])

    def test_startup_created_with_created_datetime(self):
        startup = StartupFactory()
        startup.created_at = None
        startup.save()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(startup.created_datetime, events[0]["datetime"])

    def test_startup_created_no_created_datetime(self):
        startup = StartupFactory(created_datetime=None)
        startup.created_at = None
        startup.save()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(DAWN_OF_TIME, events[0]["datetime"])

    def test_startup_created_using_other_startups(self):
        prev_created_datetime = days_from_now(-10)
        StartupFactory(created_datetime=prev_created_datetime)
        startup = StartupFactory(created_datetime=None)
        next_created_datetime = days_from_now(-2)
        StartupFactory(created_datetime=next_created_datetime)
        startup.created_at = None
        startup.save()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(prev_created_datetime, events[0]["datetime"])
            self.assertEqual(next_created_datetime,
                             events[0]["latest_datetime"])

    def test_partner_created(self):
        partner = PartnerFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[partner.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(partner.created_at, events[0]["datetime"])

    def test_partner_created_no_created_at(self):
        partner = PartnerFactory()
        partner.created_at = None
        partner.save()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[partner.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(DAWN_OF_TIME, events[0]["datetime"])

    def test_partner_created_using_later_partner(self):
        partner = PartnerFactory()
        partner.created_at = None
        partner.save()
        next_partner = PartnerFactory()
        partner_created_at = days_from_now(-2)
        next_partner.created_at = partner_created_at
        next_partner.save()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[partner.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(DAWN_OF_TIME, events[0]["datetime"])
            self.assertEqual(partner_created_at, events[0]["latest_datetime"])

    def test_organization_created(self):
        org = OrganizationFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[org.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationCreatedEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(org.created_at, events[0]["datetime"])

    def test_startup_become_entrant(self):
        cycle = ProgramCycleFactory()
        application = ApplicationFactory(
            application_status=SUBMITTED_APP_STATUS,
            application_type=cycle.default_application_type,
            cycle=cycle)
        startup = application.startup
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationBecomeEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(cycle.name in events[0]["description"])

    def test_startup_become_entrant_no_submission_datetime(self):
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
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationBecomeEntrantEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(cycle_deadline,
                             events[0]["datetime"])

    def test_startup_become_finalist(self):
        startup = StartupFactory()
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.FINALIST,
            startup=startup)
        program = startup_status.program_startup_status.program
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationBecomeFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertTrue(program.name in events[0]["description"])

    def test_startup_become_finalist_no_created_at(self):
        startup = StartupFactory()
        start_date = days_from_now(10)
        startup_status = StartupStatusFactory(
            program_startup_status__startup_role__name=StartupRole.FINALIST,
            program_startup_status__program__start_date=start_date,
            startup=startup)
        startup_status.created_at = None
        startup_status.save()
        with self.login(username=self.basic_user().username):
            url = reverse("organization_history",
                          args=[startup.organization.id])
            response = self.client.get(url)
            events = find_events(response.data["history"],
                                 OrganizationBecomeFinalistEvent.EVENT_TYPE)
            self.assertEqual(1, len(events))
            self.assertEqual(start_date, events[0]["datetime"])
