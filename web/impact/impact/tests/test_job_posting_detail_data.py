# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v0.api_data.job_posting_detail_data import JobPostingDetailData
from impact.tests.factories import JobPostingFactory
from test_plus.test import TestCase


class TestJobPostingDetailData(TestCase):

    def test_valid_job_key_as_int(self):
        job = JobPostingFactory()
        data = JobPostingDetailData({"JobKey": job.pk})
        self.assertTrue(data.valid())
        self.assertEqual(job, data.job)

    def test_valid_job_key_as_string(self):
        job = JobPostingFactory()
        data = JobPostingDetailData({"JobKey": str(job.pk)})
        self.assertTrue(data.valid())
        self.assertEqual(job, data.job)

    def test_invalid_job_key(self):
        data = JobPostingDetailData({"JobKey": -1})
        self.assertFalse(data.valid())
