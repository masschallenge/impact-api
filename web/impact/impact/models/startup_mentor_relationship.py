# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.startup_mentor_tracking_record import (
    StartupMentorTrackingRecord,
)
from impact.models.utils import is_managed


CONFIRMED_RELATIONSHIP = "Confirmed"
DESIRED_RELATIONSHIP = "Desired"
DISCUSSING_RELATIONSHIP = "In Discussions With"
RELATIONSHIP_CHOICES = ((DESIRED_RELATIONSHIP, DESIRED_RELATIONSHIP),
                        (DISCUSSING_RELATIONSHIP, DISCUSSING_RELATIONSHIP),
                        (CONFIRMED_RELATIONSHIP, CONFIRMED_RELATIONSHIP))


class StartupMentorRelationship(MCModel):
    startup_mentor_tracking = models.ForeignKey(StartupMentorTrackingRecord)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(
        max_length=32,
        choices=RELATIONSHIP_CHOICES,
        default=DESIRED_RELATIONSHIP)
    primary = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_startupmentorrelationship'
        managed = is_managed(db_table)
        verbose_name_plural = 'Startup Mentor Relationships'

    def __str__(self):
        name = "Relationship of %s to %s" % (
            self.startup_mentor_tracking.startup.name,
            self.mentor.get_profile().full_name()
        )
        return name
