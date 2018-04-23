# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import V0APIPermissions
from impact.v0.api_data.job_posting_detail_data import (
    JobPostingDetailData,
    job_type_description,
)
from impact.v0.views.utils import (
    base_program_url,
    encrypt_image_token,
)


class JobPostingDetailView(APIView):
    permission_classes = (V0APIPermissions,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request):
        self.data = JobPostingDetailData(request.data)
        if self.data.valid() and self.data.job is not None:
            return Response(self._calc_result())
        else:
            return Response(status=400, data=self.data.errors)

    def _calc_result(self):
        job = self.data.job
        program = job.startup.startupstatus_set.latest(
            "id").program_startup_status.program
        if job.startup.high_resolution_logo:
            image_token = encrypt_image_token(
                job.startup.high_resolution_logo.name)
        else:
            image_token = ""
        url = ""
        if job.startup.is_visible:
            url = base_program_url(program) + job.startup.organization.url_slug
        job_data = {"startup_name": job.startup.name,
                    "startup_profile_url": url,
                    "startup_logo_image_token": image_token,
                    "title": job.title,
                    "type": job_type_description(job.type),
                    "application_email": job.applicationemail,
                    "more_info_url": job.more_info_url,
                    "description": job.description,
                    "post_date": job.postdate.strftime("%Y-%m-%d"),
                    "jobkey": job.pk,
                    }
        return job_data
