# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse

from impact.v0.api_data.startup_list_data import StartupListData as Data
from impact.tests.api_v0_test_case import APIV0TestCase
from impact.tests.factories import (
    IndustryFactory,
    ProgramFactory,
    ProgramStartupStatusFactory,
    SiteProgramAuthorizationFactory,
    StartupFactory,
    StartupStatusFactory,
)
from impact.tests.utils import match_errors
from impact.v0.views.utils import BADGE_DISPLAYS


TEST_BADGE_DISPLAY = BADGE_DISPLAYS[0]
EMPTY_RESPONSE = {'startups': []}
INVALID_DATA = {
    "ProgramKey": "123",
    "StartupStatus": "ABC",
    "GroupBy": "DEF",
    "IncludeAllGroup": "G",
    "OrderBy": "HIJ"
}

INVALID_STATUS_GROUP = "Test2 Group"
INVALID_STATUS_GROUP_DATA = {
    "GroupBy": "%s%s" % (Data.STATUS_GROUP_PREFIX,
                         INVALID_STATUS_GROUP),
    "IncludeAllGroup": Data.YES_NO_VALUES[1],
    "OrderBy": Data.ORDER_BY_VALUES[1],
}

VALID_STATUS_GROUP = "Test Group"
VALID_STATUS_GROUP_DATA = {
    "GroupBy": "%s%s" % (Data.STATUS_GROUP_PREFIX,
                         VALID_STATUS_GROUP),
    "IncludeAllGroup": Data.YES_NO_VALUES[1],
    "OrderBy": Data.ORDER_BY_VALUES[1],
}

STARTUP_LOGO = "logo.jpg"
REMOTE_LOGO = "http://cloud.test.com/logo.jpg"


class TestStartupListView(APIV0TestCase):
    def test_program_key_post(self):
        program = ProgramFactory()
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id})
            assert EMPTY_RESPONSE == response.data

    def test_program_key_with_startup(self):
        startup = StartupFactory(high_resolution_logo=STARTUP_LOGO)
        program = SiteProgramAuthorizationFactory().program
        StartupStatusFactory(
            program_startup_status__program=program,
            program_startup_status__badge_display=TEST_BADGE_DISPLAY,
            startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id})
            assert startup.name == response.data["startups"][0]["name"]
            assert STARTUP_LOGO in response.data["startups"][0]["logo_url"]

    def test_startup_with_remote_logo(self):
        startup = StartupFactory(high_resolution_logo=REMOTE_LOGO)
        program = SiteProgramAuthorizationFactory().program
        StartupStatusFactory(
            program_startup_status__program=program,
            program_startup_status__badge_display=TEST_BADGE_DISPLAY,
            startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id})
            assert startup.name == response.data["startups"][0]["name"]
            assert REMOTE_LOGO == response.data["startups"][0]["logo_url"]

    def test_startup_with_upper_case_remote_logo(self):
        logo = REMOTE_LOGO.upper()
        startup = StartupFactory(high_resolution_logo=logo)
        program = SiteProgramAuthorizationFactory().program
        StartupStatusFactory(
            program_startup_status__program=program,
            program_startup_status__badge_display=TEST_BADGE_DISPLAY,
            startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id})
            assert startup.name == response.data["startups"][0]["name"]
            assert REMOTE_LOGO.upper() == logo

    def test_stealth_startup(self):
        startup = StartupFactory(is_visible=False,
                                 high_resolution_logo=REMOTE_LOGO)
        program = SiteProgramAuthorizationFactory().program
        StartupStatusFactory(
            program_startup_status__program=program,
            program_startup_status__include_stealth_startup_names=True,
            program_startup_status__badge_display=TEST_BADGE_DISPLAY,
            startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id})
            assert "" == response.data["startups"][0]["logo_url"]

    def test_startup_with_primary_subindustry(self):
        parent_industry = IndustryFactory()
        industry = IndustryFactory(parent=parent_industry)
        startup = StartupFactory(primary_industry=industry)
        program = SiteProgramAuthorizationFactory().program
        StartupStatusFactory(
            program_startup_status__program=program,
            program_startup_status__badge_display=TEST_BADGE_DISPLAY,
            startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id,
                                         "GroupBy": "Industry",
                                         "IncludeAllGroup": Data.NO})
            industry_group = response.data["groups"][0]["group_title"]
            assert parent_industry.name == industry_group

    def test_random_ordering(self):
        program = SiteProgramAuthorizationFactory().program
        startups = [StartupFactory(), StartupFactory()]
        names = [startup.name for startup in startups]
        for startup in startups:
            StartupStatusFactory(
                program_startup_status__program=program,
                program_startup_status__badge_display=TEST_BADGE_DISPLAY,
                startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id,
                                         "OrderBy": "Random"})
            name0 = response.data["startups"][0]["name"]
            name1 = response.data["startups"][1]["name"]
            assert name0 in names
            assert name1 in names
            assert name0 != name1

    def test_alpha_asc_ordering(self):
        program = SiteProgramAuthorizationFactory().program
        startups = [StartupFactory(), StartupFactory()]
        names = sorted([startup.name for startup in startups])
        for startup in startups:
            StartupStatusFactory(
                program_startup_status__program=program,
                program_startup_status__badge_display=TEST_BADGE_DISPLAY,
                startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id,
                                         "OrderBy": "AlphaAsc"})
            assert names[0] == response.data["startups"][0]["name"]
            assert names[1] == response.data["startups"][1]["name"]

    def test_alpha_dsc_ordering(self):
        program = SiteProgramAuthorizationFactory().program
        startups = [StartupFactory(), StartupFactory()]
        names = sorted([startup.name for startup in startups])
        for startup in startups:
            StartupStatusFactory(
                program_startup_status__program=program,
                program_startup_status__badge_display=TEST_BADGE_DISPLAY,
                startup=startup)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url,
                                        {"ProgramKey": program.id,
                                         "OrderBy": "AlphaDsc"})
            assert names[0] == response.data["startups"][1]["name"]
            assert names[1] == response.data["startups"][0]["name"]

    def test_valid_args_post(self):
        program_startup_status = ProgramStartupStatusFactory(
            startup_list_include=True,
            badge_display=TEST_BADGE_DISPLAY,
            status_group=VALID_STATUS_GROUP)
        status = StartupStatusFactory(
            program_startup_status=program_startup_status)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            data = {
                "StartupStatus": program_startup_status.startup_list_tab_id,
                "ProgramKey": program_startup_status.program.name
                }
            response = self.client.post(url, data=data)
            assert status.startup.name == response.data["startups"][0]["name"]

    def test_invalid_status_group(self):
        program_startup_status = ProgramStartupStatusFactory(
            startup_list_include=True,
            badge_display=TEST_BADGE_DISPLAY,
            status_group=VALID_STATUS_GROUP)
        StartupStatusFactory(program_startup_status=program_startup_status)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            data = {
                "StartupStatus": program_startup_status.startup_list_tab_id,
                "ProgramKey": program_startup_status.program.name
            }
            data.update(INVALID_STATUS_GROUP_DATA)
            response = self.client.post(url, data=data)
            assert match_errors(
                {"StatusGroup": "%s%s" % (Data.STATUS_GROUP_PREFIX,
                                          INVALID_STATUS_GROUP)},
                response.data)

    def test_invalid_args_post(self):
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            response = self.client.post(url, data=INVALID_DATA)
            assert 404 == response.status_code
            assert match_errors(INVALID_DATA, response.data)

    def test_valid_industry_groups_post(self):
        program_startup_status = ProgramStartupStatusFactory(
            startup_list_include=True,
            badge_display=TEST_BADGE_DISPLAY,
            status_group=VALID_STATUS_GROUP)
        startup = StartupStatusFactory(
            program_startup_status=program_startup_status).startup
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            data = {
                "StartupStatus": program_startup_status.startup_list_tab_id,
                "ProgramKey": program_startup_status.program.name
                }
            data.update(VALID_STATUS_GROUP_DATA)
            data["GroupBy"] = Data.INDUSTRY_GROUP_BY
            response = self.client.post(url, data=data)
            groups = response.data["groups"]
            industry_response = groups[0]
            assert (startup.primary_industry.name ==
                    industry_response["group_title"])
            assert (startup.name ==
                    industry_response["startups"][0]["name"])

    def test_valid_industry_post_with_all(self):
        program_startup_status = ProgramStartupStatusFactory(
            startup_list_include=True,
            badge_display=TEST_BADGE_DISPLAY,
            status_group=VALID_STATUS_GROUP)
        StartupStatusFactory(program_startup_status=program_startup_status)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            data = {
                "StartupStatus": program_startup_status.startup_list_tab_id,
                "ProgramKey": program_startup_status.program.name
            }
            data.update(VALID_STATUS_GROUP_DATA)
            data["GroupBy"] = Data.INDUSTRY_GROUP_BY
            data["IncludeAllGroup"] = Data.YES
            response = self.client.post(url, data=data)
            groups = response.data["groups"]
            assert len(groups) == 2
            assert Data.ALL_INDUSTRY == groups[0]["group_title"]

    def test_status_fields(self):
        program_startup_status = ProgramStartupStatusFactory(
            startup_list_include=True,
            badge_display=TEST_BADGE_DISPLAY,
            status_group=VALID_STATUS_GROUP)
        StartupStatusFactory(
            program_startup_status=program_startup_status)
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            data = {
                "StartupStatus": program_startup_status.startup_list_tab_id,
                "ProgramKey": program_startup_status.program.name,
                "GroupBy": Data.INDUSTRY_GROUP_BY,
                }
            response = self.client.post(url, data=data)
            assert (program_startup_status.startup_list_tab_title ==
                    response.data["status"])
            assert (program_startup_status.startup_list_tab_description ==
                    response.data["status_description"])

    def test_valid_status_groups_post(self):
        program_startup_status = ProgramStartupStatusFactory(
            startup_list_include=True,
            badge_display=TEST_BADGE_DISPLAY,
            status_group=VALID_STATUS_GROUP)
        startup = StartupStatusFactory(
            program_startup_status=program_startup_status).startup
        with self.login(username=self.basic_user().username):
            url = reverse("startup_list")
            data = {
                "StartupStatus": program_startup_status.startup_list_tab_id,
                "ProgramKey": program_startup_status.program.name
            }
            data.update(VALID_STATUS_GROUP_DATA)
            response = self.client.post(url, data=data)
            groups = response.data["groups"]
            status_group_response = groups[0]
            assert (VALID_STATUS_GROUP_DATA["GroupBy"] ==
                    "%s%s" % (Data.STATUS_GROUP_PREFIX,
                              status_group_response["group_title"]))
            assert (startup.name ==
                    status_group_response["startups"][0]["name"])
