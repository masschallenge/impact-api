# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

try:
    from ordered_model.models import OrderedModel
    HAS_ORDERED_MODEL = True
except ImportError:
    HAS_ORDERED_MODEL = False

from impact.models.program import Program
from impact.models.startup import Startup
from impact.models.utils import is_managed

import logging
logger = logging.getLogger(__file__)


INTEREST_CHOICES = [
    ("g", "Definitely will participate"),
    ("w", "Will participate"),
    ("p", "Likely will participate"),
    ("n", "Might not participate"),
    ("l", "Likely won't participate"),
]


PROGRAM_INTEREST_BOTTOM = 'bottom'
PROGRAM_INTEREST_TOP = 'top'
PROGRAM_INTEREST_UP = 'up'
PROGRAM_INTEREST_DOWN = 'down'

EXTRA_INTERESTS = ("%s interests in program %s for startup %s found. "
                   "Only expected 1.")


if HAS_ORDERED_MODEL:
    cls = OrderedModel
    meta = OrderedModel.Meta
else:
    cls = models.Model
    meta = object


class StartupProgramInterest(cls):
    program = models.ForeignKey(Program)
    startup = models.ForeignKey(Startup)
    startup_cycle_interest = models.ForeignKey(
        "StartupCycleInterest", blank=True, null=True)
    applying = models.BooleanField(default=False)
    interest_level = models.CharField(
        max_length=64,
        choices=INTEREST_CHOICES,
        blank=True,
        null=True
    )

    if not HAS_ORDERED_MODEL:
        order = models.IntegerField()

    class Meta:
        db_table = 'mc_startupprograminterest'
        managed = is_managed(db_table)
        ordering = ['order']
