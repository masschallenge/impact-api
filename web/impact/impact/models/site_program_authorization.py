# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.site import Site
from impact.models.program import Program
from impact.models.utils import is_managed


class SiteProgramAuthorization(MCModel):
    site = models.ForeignKey(Site)
    program = models.ForeignKey(Program)
    startup_profile_base_url = models.URLField()
    sponsor_profile_base_url = models.URLField()
    video_base_url = models.URLField()

    startup_list = models.BooleanField(default=False)
    startup_profiles = models.BooleanField(default=False)
    startup_team_members = models.BooleanField(default=False)
    mentor_list = models.BooleanField(default=False)
    videos = models.BooleanField(default=False)
    sponsor_list = models.BooleanField(default=False)
    sponsor_profiles = models.BooleanField(default=False)
    sponsor_logos = models.BooleanField(default=False)
    jobs = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_siteprogramauthorization'
        managed = is_managed(db_table)
        unique_together = (("site", "program"), )
        verbose_name_plural = 'Site Program Authorizations'
