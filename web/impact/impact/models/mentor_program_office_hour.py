# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.utils import is_managed

MC_BOS_LOCATION = "MassChallenge Boston"
MC_CH_LOCATION = "MassChallenge Switzerland"
MC_IL_JLM_LOCATION = "MassChallenge Israel - Jerusalem"
MC_IL_TLV_LOCATION = "MassChallenge Israel - Tel Aviv"
MC_MX_LOCATION = "MassChallenge Mexico"
MC_NIC_LOCATION = "Newton Innovation Center (NIC)"
MC_PULSE_LOCATION = "Pulse@MassChallenge"
MC_REMOTE_LOCATION = "Remote"
LOCATION_CHOICES = (
    (MC_BOS_LOCATION, MC_BOS_LOCATION),
    (MC_IL_JLM_LOCATION, MC_IL_JLM_LOCATION),
    (MC_IL_TLV_LOCATION, MC_IL_TLV_LOCATION),
    (MC_CH_LOCATION, MC_CH_LOCATION),
    (MC_MX_LOCATION, MC_MX_LOCATION),
    (MC_PULSE_LOCATION, MC_PULSE_LOCATION),
    (MC_NIC_LOCATION, MC_NIC_LOCATION),
    (MC_REMOTE_LOCATION, MC_REMOTE_LOCATION),
)


class MentorProgramOfficeHour(MCModel):
    program = models.ForeignKey(Program)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='mentor_officehours')
    finalist = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name="Finalist",
                                 blank=True,
                                 null=True,
                                 related_name='finalist_officehours')
    date = models.DateField(db_index=True)
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField(db_index=True)
    description = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    notify_reservation = models.BooleanField(default=True)
    topics = models.CharField(max_length=500, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_mentorprogramofficehour'
        managed = is_managed(db_table)
        verbose_name = "Office Hour"
        unique_together = ('program', 'mentor', 'date', 'start_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        hour_type = "Reserved"
        if self.is_open():
            hour_type = "Open"
        return "%s office hour with %s" % (hour_type, self.mentor)
