# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings
from django.urls import reverse

from impact.tests.factories import (
    IndustryFactory,
    ProgramFactory,
    StartupFactory,
    StartupStatusFactory,
    StartupTeamMemberFactory,
)
from impact.tests.contexts import UserContext
from impact.tests.utils import match_errors
from impact.tests.api_test_case import APITestCase
from impact.v0.views.startup_detail_view import EMPTY_DETAIL_RESULT
from impact.v0.views.utils import BADGE_DISPLAYS


EMPTY_RESPONSE = {'startups': []}
VIMEO_EXAMPLE = "https://vimeo.com/149212783"
BAD_YOUTUBE_EXAMPLE = "https://www.youtube.com/x/y/z"
UNKNOWN_VIDEO_EXAMPLE = "http://blahblahblah.com/149212783"
STARTUP_DETAIL_URL = reverse("startup_detail")


class TestStartupDetailView(APITestCase):

    def test_basic_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(user=context.user)
        startup = member.startup
        startup.additional_industries.add(IndustryFactory())
        program = ProgramFactory()
        program_status = StartupStatusFactory(
            program_startup_status__program=program,
            program_startup_status__badge_display=BADGE_DISPLAYS[0],
            program_startup_status__startup_list_include=True,
            startup=startup).program_startup_status.startup_status
        other_status = StartupStatusFactory(
            program_startup_status__program=ProgramFactory(),
            program_startup_status__badge_display=BADGE_DISPLAYS[0],
            program_startup_status__startup_list_include=True,
            startup=startup).program_startup_status.startup_status
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            assert startup.name == response.data["name"]
            statuses = [status["status_name"]
                        for status in response.data["statuses"]]
            assert program_status in statuses
            assert other_status not in statuses

    def test_post_without_program(self):
        context = UserContext()
        member = StartupTeamMemberFactory(user=context.user)
        startup = member.startup
        status1 = StartupStatusFactory(
            program_startup_status__badge_display=BADGE_DISPLAYS[0],
            program_startup_status__startup_list_include=True,
            startup=startup).program_startup_status.startup_status
        status2 = StartupStatusFactory(
            program_startup_status__badge_display=BADGE_DISPLAYS[0],
            program_startup_status__startup_list_include=True,
            startup=startup).program_startup_status.startup_status
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"StartupKey": startup.id})
            assert startup.name == response.data["name"]
            statuses = [status["status_name"]
                        for status in response.data["statuses"]]
            assert status1 in statuses
            assert status2 in statuses

    def test_stealth_startup_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(user=context.user,
                                          startup__is_visible=False)
        startup = member.startup
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            assert EMPTY_DETAIL_RESULT == response.data

    def test_url_slug_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(user=context.user)
        startup = member.startup
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(
                STARTUP_DETAIL_URL,
                {"ProgramKey": program.id,
                 "StartupKey": startup.organization.url_slug})
            assert startup.name == response.data["name"]

    def test_public_member_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(user=context.user,
                                          display_on_public_profile=True)
        startup = member.startup
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            assert startup.name == response.data["name"]

    def test_recognized_video_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(
            user=context.user,
            display_on_public_profile=True,
            startup__video_elevator_pitch_url=VIMEO_EXAMPLE)
        startup = member.startup
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            assert "iframe" in response.data["video_elevator_pitch_url"]

    def test_bad_video_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(
            user=context.user,
            display_on_public_profile=True,
            startup__video_elevator_pitch_url=BAD_YOUTUBE_EXAMPLE)
        startup = member.startup
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            assert "" == response.data["video_elevator_pitch_url"]

    def test_unrecognized_video_post(self):
        context = UserContext()
        member = StartupTeamMemberFactory(
            user=context.user,
            display_on_public_profile=True,
            startup__video_elevator_pitch_url=UNKNOWN_VIDEO_EXAMPLE)
        startup = member.startup
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            assert "" == response.data["video_elevator_pitch_url"]

    def test_deleted_startup(self):
        startup = StartupFactory()
        startup_id = startup.id
        startup.delete()
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup_id})
            assert response.status_code == 404
            assert match_errors({"StartupKey": str(startup_id)},
                                response.data)

    def test_missing_startup(self):
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id})
            assert response.status_code == 404
            assert match_errors({"StartupKey": "'None'"},
                                response.data)

    def test_logos_are_resized(self):
        path = "startup_pics/yuge.png"
        context = UserContext()
        member = StartupTeamMemberFactory(user=context.user)
        startup = member.startup
        startup.high_resolution_logo = path
        startup.save()
        program = ProgramFactory()
        with self.login(email=self.basic_user().email):
            response = self.client.post(STARTUP_DETAIL_URL,
                                        {"ProgramKey": program.id,
                                         "StartupKey": startup.id})
            url_base = (settings.IMAGE_RESIZE_HOST +
                        settings.IMAGE_RESIZE_TEMPLATE).format("")
            self.assertTrue(url_base in response.data["logo_url"])
