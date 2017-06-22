# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.api_data import APIData
from .job_posting_detail_data import JOB_TYPES


class JobPostingListData(APIData):

    def valid(self):
        self.job_type = self._validate_job_type()
        self.keywords = self._validate_keywords()
        self.order_by = self._validate_order_by()
        self.program = self.validate_program(required=False)
        self.startup = self.validate_startup(required=False)
        return self.errors == []

    def _validate_job_type(self):
        job_type = self.data.get("JobType", None)
        if job_type is None:
            return
        elif job_type not in JOB_TYPES:
            self.record_invalid_value(job_type, "JobType")
        else:
            return job_type

    def _validate_keywords(self):
        keywords = self.data.get("Keywords", None)
        if keywords is not None:
            # Doubled or leading/trailing commas produce empty-string values.
            # This list comp drops them.
            keywords = [k.strip() for k in keywords.split(",") if k.strip()]
        # Currently, we consider all keywords valid
        return keywords

    def _validate_order_by(self):
        order_by = self.data.get("OrderBy", "postdatedesc").lower()
        if order_by not in ["jobtype", "postdatedesc", "startup"]:
            self.record_invalid_value(order_by, "OrderBy")
            return
        else:
            return order_by
