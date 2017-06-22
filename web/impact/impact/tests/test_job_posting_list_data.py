# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v0.api_data.job_posting_list_data import JobPostingListData
from test_plus.test import TestCase


class TestJobPostingListData(TestCase):

    def test_valid_job_type(self):
        data = JobPostingListData({"JobType": "INTERNSHIP"})
        self.assertTrue(data.valid())

    def test_invalid_job_type(self):
        data = JobPostingListData({"JobType": "X"})
        self.assertFalse(data.valid())

    def test_valid_order_by(self):
        data = JobPostingListData({"OrderBy": "postdatedesc"})
        self.assertTrue(data.valid())

    def test_invalid_order_by(self):
        data = JobPostingListData({"OrderBy": "X"})
        self.assertFalse(data.valid())

    def test_keyword_processing(self):
        data = JobPostingListData({"Keywords": " , a,,b , c,,"})
        data.valid()
        self.assertEqual(data.keywords, ["a", "b", "c"])
