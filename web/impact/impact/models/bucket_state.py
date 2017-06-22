# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program_role import ProgramRole
from impact.models.program_cycle import ProgramCycle
from impact.models.utils import is_managed


NEW_ENTREPRENEURS_BUCKET_TYPE = "new_entrepreneurs"
STALE_NOSTARTUP_BUCKET_TYPE = "stale_nostartup"
STALE_STARTUP_BUCKET_TYPE = "stale_startup"
UNPAID_BUCKET_TYPE = "unpaid"
UNSUBMITTED_BUCKET_TYPE = "unsubmitted"
SUBMITTED_BUCKET_TYPE = "submitted"
BUCKET_TYPES = (
    (STALE_NOSTARTUP_BUCKET_TYPE, "Old Entrepreneurs"),
    (STALE_STARTUP_BUCKET_TYPE, "Old Startups"),
    (NEW_ENTREPRENEURS_BUCKET_TYPE, "New Entrepreneurs"),
    (UNPAID_BUCKET_TYPE, "Active Unpaid Startups"),
    (UNSUBMITTED_BUCKET_TYPE, "Working on Application"),
    (SUBMITTED_BUCKET_TYPE, "Has Submitted Application"),
)


class BucketState(MCModel):
    name = models.CharField(
        max_length=64,
        choices=BUCKET_TYPES,
        null=True,
        blank=True,
        default="unsubmitted",
    )
    group = models.CharField(max_length=255,
                             default="Other")
    sort_order = models.PositiveIntegerField()
    cycle = models.ForeignKey(ProgramCycle)
    last_update = models.DateTimeField()
    program_role = models.ForeignKey(ProgramRole)

    class Meta(MCModel.Meta):
        db_table = 'mc_bucketstate'
        managed = is_managed(db_table)
        ordering = ["sort_order", ]

    def __str__(self):
        return self.name
