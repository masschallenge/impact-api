# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.startup import Startup
from impact.models.utils import is_managed

JOB_TYPE_VALUES = (('NONE', 'None'),
                   ('INTERNSHIP', 'An internship'),
                   ('PART_TIME_PERMANENT', 'A part-time permanent position'),
                   ('FULL_TIME_PERMANENT', 'A full-time permanent position'),
                   ('PART_TIME_CONTRACT', 'A part-time contract position'),
                   ('FULL_TIME_CONTRACT', 'A full-time contract position'))


class JobPosting(MCModel):
    startup = models.ForeignKey(Startup)
    postdate = models.DateTimeField(blank=False)
    type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_VALUES)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    applicationemail = models.EmailField(verbose_name="Email address",
                                         max_length=100, null=True, blank=True)
    more_info_url = models.URLField(max_length=100, null=True, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_jobposting'
        managed = is_managed(db_table)
        verbose_name_plural = 'Job postings for startups'

    def __str__(self):
        return "%s at %s" % (self.title, self.startup.name)
