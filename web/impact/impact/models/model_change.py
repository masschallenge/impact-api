from django.db import models
from impact.models.mc_model import MCModel

MIGRATION_STATUS_OLD = "OLD"
MIGRATION_STATUS_MIGRATING = "MIGRATING"
MIGRATION_STATUS_DONE = "DONE"
MIGRATION_STATUS_ERROR = "ERROR"

MODEL_CHANGE_STATUSES = [
    MIGRATION_STATUS_OLD,
    MIGRATION_STATUS_MIGRATING,
    MIGRATION_STATUS_DONE,
    MIGRATION_STATUS_ERROR,
]

MODEL_CHANGE_STATUS_CHOICES = [(x, x) for x in MODEL_CHANGE_STATUSES]


class ModelChange(MCModel):
    name = models.CharField(max_length=128, unique=True)
    status = models.CharField(max_length=64,
                              choices=MODEL_CHANGE_STATUS_CHOICES,
                              default=MIGRATION_STATUS_OLD)

    def __str__(self):
        return "{} ({})".format(self.name, self.status)
