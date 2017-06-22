# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from pytz import utc
from datetime import (
    datetime,
    timedelta,
)
import json
from django.urls import reverse

from impact.tests.api_v0_test_case import APIV0TestCase
from impact.models import (
    JobPosting,
    Site,
    Startup,
)

from impact.tests.factories import (
    JobPostingFactory,
    ProgramFactory,
    ProgramStartupStatusFactory,
    SiteProgramAuthorizationFactory,
    StartupFactory,
    StartupStatusFactory,
)


class TestJobPostingListView(APIV0TestCase):

    def setUp(self):
        # Many objects must be created to scaffold this thing
        Site.objects.create()
        _site = Site.objects.first()
        startup1, startup2 = StartupFactory.create_batch(2)
        startup1.high_resolution_logo = "hamsterdance.gif"
        startup1.save()
        JobPostingFactory(startup=startup1)
        JobPostingFactory(startup=startup2)
        self.program = ProgramFactory()
        _pss = ProgramStartupStatusFactory(program=self.program)
        StartupStatusFactory(startup=startup1,
                             program_startup_status=_pss)
        StartupStatusFactory(startup=startup2,
                             program_startup_status=_pss)
        SiteProgramAuthorizationFactory(site=_site, program=self.program)
        self.url = reverse("job_posting_list")

    def test_all_jobs_returned_when_no_program_key(self):
        with self.login(username=self.basic_user().username):
            response = self.client.post(self.url)
            response_data = json.loads(response.content)["job_postings"]
            self.assertEqual(2, len(response_data))

    def test_filter_by_startup(self):
        startup = Startup.objects.first()
        with self.login(username=self.basic_user().username):
            data = {"StartupKey": startup.pk}
            response = self.client.post(self.url, data=data)
            response_data = json.loads(response.content)["job_postings"][0]
            self.assertEqual(response_data["startup_name"], startup.name)

    # Default ordering should be by post_date, descending
    def test_ordering_default(self):
        j1 = JobPosting.objects.first()
        j1.postdate = utc.localize(datetime.now())
        j1.save()
        j2 = JobPosting.objects.last()
        j2.postdate = utc.localize(datetime.now() - timedelta(1))
        j2.save()
        with self.login(username=self.basic_user().username):
            response = self.client.post(self.url)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(jobs[0]["post_date"] > jobs[1]["post_date"])

    def test_ordering_by_type(self):
        with self.login(username=self.basic_user().username):
            data = {"OrderBy": "jobtype"}
            response = self.client.post(self.url, data=data)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(jobs[0]["type"] < jobs[1]["type"])

    def test_ordering_by_startup(self):
        with self.login(username=self.basic_user().username):
            data = {"OrderBy": "startup"}
            response = self.client.post(self.url, data=data)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(jobs[0]["startup_name"] < jobs[1]["startup_name"])

    def test_valid_programkey(self):
        with self.login(username=self.basic_user().username):
            response = self.client.post(
                self.url, data={"ProgramKey": self.program.pk})
            self.assertEqual(200, response.status_code)

    def test_invalid_programkey(self):
        with self.login(username=self.basic_user().username):
            # Bogus ProgramKey
            response = self.client.post(self.url, data={"ProgramKey": "x"})
            self.assertEqual(400, response.status_code)

    def test_filter_on_keywords(self):
        # Tweak a couple jobs to have values we want
        j1 = JobPosting.objects.first()
        j1.title = "Strategerist"
        j1.save()
        j2 = JobPosting.objects.last()
        j2.description = "enterprisey"
        j2.save()
        with self.login(username=self.basic_user().username):
            # Match on title
            data = {"Keywords": "Strategerist"}
            response = self.client.post(self.url, data=data)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(len(jobs) == 1)
            # Match on description
            data = {"Keywords": "enterprisey"}
            response = self.client.post(self.url, data=data)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(len(jobs) == 1)

    def test_filter_on_jobtype(self):
        # Tweak a couple jobs to have values we want
        j1 = JobPosting.objects.first()
        j1.type = "INTERNSHIP"
        j1.save()
        j2 = JobPosting.objects.last()
        j2.type = "PART_TIME_PERMANENT"
        j2.save()
        with self.login(username=self.basic_user().username):
            # Match on title
            data = {"JobType": "INTERNSHIP"}
            response = self.client.post(self.url, data=data)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(len(jobs) == 1)
            # Match on description
            data = {"JobType": "PART_TIME_PERMANENT"}
            response = self.client.post(self.url, data=data)
            jobs = json.loads(response.content)["job_postings"]
            self.assertTrue(len(jobs) == 1)
