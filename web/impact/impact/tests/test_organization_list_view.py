# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.models import (
    Organization
)
from impact.tests.factories import (
    PartnerFactory,
    OrganizationFactory,
    StartupFactory,
)
import datetime
from impact.tests.api_test_case import APITestCase
from impact.v1.views.organization_list_view import serialize_org
import simplejson as json
import pytz


class TestOrganizationListView(APITestCase):

    def test_get_startup(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        with self.login(username=self.basic_user().username):
            url = reverse("organization")
            response = self.client.get(url)
            assert response.data['count'] == count
            assert all([serialize_org(startup.organization)
                        in response.data['results']
                        for startup in startups])

    def test_get_partner(self):
        count = 5
        partners = PartnerFactory.create_batch(count)
        with self.login(username=self.basic_user().username):
            url = reverse("organization")
            response = self.client.get(url)
            assert response.data['count'] == count
            assert all([serialize_org(partner.organization)
                        in response.data['results']
                        for partner in partners])

    def test_updated_at_lt_datetime_filter(self):
        count = 5
        organizations = OrganizationFactory.create_batch(count)
        response = ""
        lastweek = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        Organization.objects.filter(id__in=[
            organizations[0].id,
            organizations[1].id]).update(
            updated_at=lastweek)
        with self.login(username=self.basic_user().username):
            url = "{base_url}?updated_at__lt={datestr}".format(
                base_url=reverse("organization"),
                datestr=lastweek.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['count'], 0)

    def test_updated_at_gt_datetime_filter(self):
        count = 5
        organizations = OrganizationFactory.create_batch(count)
        response = ""
        lastweek = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        Organization.objects.filter(id__in=[
            organizations[0].id,
            organizations[1].id]).update(
            updated_at=lastweek)
        with self.login(username=self.basic_user().username):
            url = "{base_url}?updated_at__gt={datestr}".format(
                base_url=reverse("organization"),
                datestr=lastweek.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
        json_response = json.loads(response.content)
        contains_organization = False
        for result in json_response['results']:
            if result['id'] == organizations[0].id:
                contains_organization = True
                break
        self.assertTrue(contains_organization)
