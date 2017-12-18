# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import datetime
import json
from jsonschema import Draft4Validator
import pytz

from django.urls import reverse

from impact.tests.factories import (
    PartnerFactory,
    OrganizationFactory,
    StartupFactory,
)
from impact.tests.api_test_case import APITestCase
from impact.tests.test_organization_detail_view import (
    PARTNER_GET_FIELDS,
    STARTUP_GET_FIELDS,
)
from impact.tests.utils import (
    assert_fields,
)
from impact.utils import override_updated_at
from impact.v1.views import OrganizationListView


class TestOrganizationListView(APITestCase):
    url = reverse(OrganizationListView.view_name)

    def test_get_startup(self):
        count = 5
        startups = StartupFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data['count'] == count
            assert all([OrganizationListView.serialize(startup.organization)
                        in response.data['results']
                        for startup in startups])

    def test_get_partner(self):
        count = 5
        partners = PartnerFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            response = self.client.get(self.url)
            assert response.data['count'] == count
            assert all([OrganizationListView.serialize(partner.organization)
                        in response.data['results']
                        for partner in partners])

    def test_get_with_limit(self):
        count = 5
        StartupFactory.create_batch(count)
        with self.login(email=self.basic_user().email):
            limit = 2
            url = self.url + "?limit=%s" % limit
            response = self.client.get(url)
            assert response.data['count'] == count
            assert len(response.data['results']) == limit

    def test_updated_at_before_datetime_filter(self):
        updated_none = _org_for_date(None)
        week_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        one_day = datetime.timedelta(days=1)
        updated_before = _org_for_date(week_ago - one_day)
        updated_exactly = _org_for_date(week_ago)
        updated_after = _org_for_date(week_ago + one_day)
        with self.login(email=self.basic_user().email):
            url = "{base_url}?updated_at.before={datestr}".format(
                base_url=self.url,
                datestr=week_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
            assert _contains_org(updated_none, response.data)
            assert _contains_org(updated_before, response.data)
            assert _contains_org(updated_exactly, response.data)
            assert not _contains_org(updated_after, response.data)

    def test_updated_at_after_datetime_filter(self):
        updated_none = _org_for_date(None)
        week_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        one_day = datetime.timedelta(days=1)
        updated_before = _org_for_date(week_ago - one_day)
        updated_exactly = _org_for_date(week_ago)
        updated_after = _org_for_date(week_ago + one_day)
        with self.login(email=self.basic_user().email):
            url = "{base_url}?updated_at.after={datestr}".format(
                base_url=self.url,
                datestr=week_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            response = self.client.get(url)
            assert not _contains_org(updated_none, response.data)
            assert not _contains_org(updated_before, response.data)
            assert _contains_org(updated_exactly, response.data)
            assert _contains_org(updated_after, response.data)

    def test_options(self):
        with self.login(email=self.basic_user().email):
            response = self.client.options(self.url)
            assert response.status_code == 200
            results = response.data["actions"]["GET"]["properties"]["results"]
            get_options = results["item"]["properties"]
            assert_fields(PARTNER_GET_FIELDS, get_options)
            assert_fields(STARTUP_GET_FIELDS, get_options)

    def test_options_against_get(self):
        with self.login(email=self.basic_user().email):
            options_response = self.client.options(self.url)
            get_response = self.client.get(self.url)

            schema = options_response.data["actions"]["GET"]
            validator = Draft4Validator(schema)
            assert validator.is_valid(json.loads(get_response.content))

    def test_results_are_filtered_by_name(self):
        name = "foo"
        other_name = "bar"
        startup = StartupFactory(organization__name=name)
        other_startup = StartupFactory(organization__name=other_name)
        with self.login(email=self.basic_user().email):
            url = self.url + "?name=%s" % name
            response = self.client.get(url)
            assert response.data['count'] == 1
            assert _contains_org(startup.organization, response.data)
            assert not _contains_org(other_startup.organization, response.data)

    def test_next_info_contains_filter(self):
        name = "foo"
        StartupFactory(organization__name=name)
        StartupFactory.create_batch(20)
        with self.login(email=self.basic_user().email):
            name_query_parameter = "name=%s" % name
            url = self.url + "?" + name_query_parameter
            response = self.client.get(url)
            assert name_query_parameter in response.data['next']


def _org_for_date(date):
    org = OrganizationFactory()
    override_updated_at(org, date)
    return org


def _contains_org(org, data):
    for result in data["results"]:
        if result["id"] == org.id:
            return True
    return False
