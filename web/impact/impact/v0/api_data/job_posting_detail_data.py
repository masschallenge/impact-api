# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.api_data import APIData
from accelerator.models import JobPosting


JOB_TYPES = {"NONE": "None",
             "INTERNSHIP": "An internship",
             "PART_TIME_PERMANENT": "A part-time permanent position",
             "FULL_TIME_PERMANENT": "A full-time permanent position",
             "PART_TIME_CONTRACT": "A part-time contract position",
             "FULL_TIME_CONTRACT": "A full-time contract position"
             }


def job_type_description(job_type):
    """Look up verbose job type label, or use key literally if no match."""
    if job_type in JOB_TYPES:
        return JOB_TYPES[job_type]
    else:
        return job_type


class JobPostingDetailData(APIData):

    def valid(self):
        self.job = self._validate_job_key()
        return self.errors == []

    def _validate_job_key(self):
        job_key = self.data.get("JobKey", None)
        if job_key is None:
            return None
        job = None
        if isinstance(job_key, int) or job_key.isdigit():
            try:
                job = JobPosting.objects.get(pk=job_key)
            except JobPosting.DoesNotExist:
                self.record_not_found(job_key, "JobKey")
        return job
