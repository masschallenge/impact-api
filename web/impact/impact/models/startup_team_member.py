# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.startup import Startup
from impact.models.recommendation_tag import RecommendationTag
from impact.models.utils import is_managed


class StartupTeamMember(MCModel):
    startup = models.ForeignKey(Startup)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=60, blank=True)
    startup_administrator = models.BooleanField(
        help_text='You have to have at least one administrator')
    is_contact = models.BooleanField(
        default=False,
        help_text='A secondary contact for the startup')
    primary_contact = models.BooleanField(
        default=False,
        help_text='You may only have one primary contact')
    technical_contact = models.BooleanField(default=False)
    marketing_contact = models.BooleanField(default=False)
    financial_contact = models.BooleanField(default=False)
    legal_contact = models.BooleanField(default=False)
    product_contact = models.BooleanField(default=False)
    design_contact = models.BooleanField(default=False)
    display_on_public_profile = models.BooleanField(default=True)
    founder = models.NullBooleanField(default=False, null=True)
    recommendation_tags = models.ManyToManyField(RecommendationTag,
                                                 blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_startupteammember'
        managed = is_managed(db_table)
        unique_together = ('startup', 'user')
        verbose_name_plural = 'Startup Team Members'

    def __str__(self):
        return "%s of %s" % (self.user.email, self.startup.name)
