# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from impact.models import (
    JobPosting,
    Site,
    SiteProgramAuthorization,
)
from impact.permissions import V0APIPermissions
from impact.utils import compose_filter
from impact.v0.api_data.job_posting_detail_data import job_type_description
from impact.v0.api_data.job_posting_list_data import JobPostingListData
from impact.v0.views.utils import (
    base_program_url,
    encrypt_image_token,
)


# ORM argument name bits for use with `compose_filter`
STARTUPS_IN_PROGRAMS = [
    "startupstatus",
    "program_startup_status",
    "program",
    "in"]


JOBS_IN_PROGRAMS = [
    "startup",
    "startupstatus",
    "program_startup_status",
    "program",
    "in"]


class JobPostingListView(APIView):
    permission_classes = (V0APIPermissions,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request):
        self.data = JobPostingListData(request.data)
        if self.data.valid():
            return Response(self._calc_result())
        return Response(status=400, data=self.data.errors)

    def _calc_result(self):
        jobs = self._get_jobs()
        program = self.data.program
        base_url = base_program_url(program)

        # Parameter `Keywords`
        if self.data.keywords:
            # Build up a big chain of Q objects, OR'd together
            query = Q()
            for kw in self.data.keywords:
                query |= Q(description__icontains=kw)
                query |= Q(title__icontains=kw)
            jobs = jobs.filter(query)

        # Parameter `JobType`
        if self.data.job_type:
            jobs = jobs.filter(type=self.data.job_type)

        # Parameter `OrderBy
        if self.data.order_by == "startup":
            jobs = jobs.order_by("startup__organization__name", "-postdate")
        elif self.data.order_by == "postdatedesc":
            jobs = jobs.order_by("-postdate", "startup__organization__name")
        elif self.data.order_by == "jobtype":
            jobs = jobs.order_by("type",
                                 "-postdate",
                                 "startup__organization__name")

        joblist = []
        for job in jobs:
            if job.startup.high_resolution_logo:
                image_token = encrypt_image_token(
                    job.startup.high_resolution_logo.name)
            else:
                image_token = ""
            url = ""
            if job.startup.is_visible:
                url = base_url + job.startup.organization.url_slug
            joblist.append({"startup_name": job.startup.name,
                            "startup_profile_url": url,
                            "startup_logo_image_token": image_token,
                            "title": job.title,
                            "type": job_type_description(job.type),
                            "application_email": job.applicationemail,
                            "more_info_url": job.more_info_url,
                            "description": job.description,
                            "post_date": job.postdate.strftime("%Y-%m-%d"),
                            "jobkey": job.pk,
                            })

        return {"job_postings": joblist}

    def _get_jobs(self):
        if self.data.startup:
            return JobPosting.objects.filter(startup=self.data.startup)
        return JobPosting.objects.filter(
            **compose_filter(JOBS_IN_PROGRAMS, self._programs())).distinct()

    def _programs(self):
        if self.data.program:
            return [self.data.program]
        site = Site.objects.first()
        return [spa.program for spa in
                SiteProgramAuthorization.objects.filter(site=site)]
