# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import (
    JobPostingFactory,
    StartupStatusFactory,
)


class TestJobPostingDetailView(APITestCase):

    def test_request_with_no_jobkey(self):
        with self.login(email=self.basic_user().email):
            url = reverse("job_posting_detail")
            # We are not passing JobKey but the view needs it
            response = self.client.post(url, data={})
            self.assertEqual(400, response.status_code)

    def test_request_with_jobkey(self):
        job = JobPostingFactory()
        StartupStatusFactory(startup=job.startup)
        with self.login(email=self.basic_user().email):
            url = reverse("job_posting_detail")
            data = {"JobKey": job.pk}
            response = self.client.post(url, data=data)
            self.assertEqual(200, response.status_code)

    def test_image_token_no_smoke(self):
        job = JobPostingFactory()
        job.startup.high_resolution_logo = "hamsterdance.gif"
        job.startup.save()
        StartupStatusFactory(startup=job.startup)
        with self.login(email=self.basic_user().email):
            url = reverse("job_posting_detail")
            data = {"JobKey": job.pk}
            response = self.client.post(url, data=data)
            self.assertEqual(200, response.status_code)
