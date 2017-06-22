# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from simpleuser.models import User

from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.startup import Startup
from impact.models.utils import is_managed

MENTOR_HELP = """
Select the Mentors you would like to work with during the program.
Start typing a Mentor's name; if they are in the Mentor Directory,
their name should appear as you type.
If you don't find the person you are looking for, use 'Other Mentors' below.
"""

OTHER_MENTOR_HELP = """
Please list Mentors you are already working with or would like to work with
who are not currently listed in the MassChallenge Mentor Directory.
You can list names, email addresses, company names, anything
that would help identify them. We very much welcome Mentors who are not
currently listed in the Mentor Directory.
"""


class StartupMentorTrackingRecord(MCModel):
    startup = models.ForeignKey(Startup)
    program = models.ForeignKey(Program)
    mentors = models.ManyToManyField(
        User,
        verbose_name="Registered Mentors",
        help_text=MENTOR_HELP,
        through="impact.StartupMentorRelationship")
    other_mentors = models.TextField(
        verbose_name="Other Mentors",
        help_text=OTHER_MENTOR_HELP,
        blank=True,
        null=True)
    notes = models.TextField(
        verbose_name="Program Goals",
        help_text="Submit the 3 goals you plan to work on with your Mentors "
        "during the Accelerator Program and report them here.",
        blank=True,
        null=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_startupmentortrackingrecord'
        managed = is_managed(db_table)
        verbose_name = "Mentor Tracking Record"
        verbose_name_plural = "Mentor Tracking Records"
        unique_together = ('startup', 'program', )

    def __str__(self):
        return "Mentor tracking record for %s" % self.startup.name
