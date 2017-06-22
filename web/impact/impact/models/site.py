# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class Site(MCModel):

    name = models.CharField(max_length=50, unique=True)
    security_key = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    site_url = models.URLField(blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_site'
        managed = is_managed(db_table)
