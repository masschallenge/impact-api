# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from .mc_model import MCModel
from .application_type import ApplicationType
from .program import Program
from .startup_label import StartupLabel
from .user_label import UserLabel
from .utils import is_managed

try:
    from .judging_round_manager import JudgingRoundManager
    HAS_MANAGER = True
except ImportError:
    HAS_MANAGER = False


ONLINE_JUDGING_ROUND_TYPE = "Online"
IN_PERSON_JUDGING_ROUND_TYPE = "In-Person"

JUDGING_ROUND_TYPE_ENUM = (
    (ONLINE_JUDGING_ROUND_TYPE, ONLINE_JUDGING_ROUND_TYPE),
    (IN_PERSON_JUDGING_ROUND_TYPE, IN_PERSON_JUDGING_ROUND_TYPE),
)

RECRUIT_NONE = "NO"
RECRUIT_ANYONE = "ANYONE"
RECRUIT_APPROVED_ONLY = "APPROVEDONLY"
RECRUIT_DISPLAY_ONLY = "DISPLAYONLY"
RECRUIT_JUDGES_ENUM = (
    (RECRUIT_NONE, 'Do not recruit judges or display prior commitments'),
    (RECRUIT_ANYONE, 'Recruit any expert'),
    (RECRUIT_APPROVED_ONLY, 'Recruit only approved judges'),
    (RECRUIT_DISPLAY_ONLY, 'Only display judges prior commitments'))

CAPTURE_AVAILABILITY_DISABLED = "disabled"
CAPTURE_AVAILABILITY_LOCATION = "location-only"
CAPTURE_AVAILABILITY_TIME = "time-only"
CAPTURE_AVAILABILITY_TIME_TYPE = "time-type"
CAPTURE_AVAILABILITY_TIME_TYPE_LOC = "time-type-location"
CAPTURE_AVAILABILITY_TYPE = "type-only"
CAPTURE_AVAILABILITY_CHOICES = (
    (CAPTURE_AVAILABILITY_DISABLED, 'Disabled'),
    (CAPTURE_AVAILABILITY_LOCATION, 'Capture location only'),
    (CAPTURE_AVAILABILITY_TIME, 'Capture time only'),
    (CAPTURE_AVAILABILITY_TIME_TYPE, 'Capture time & type'),
    (CAPTURE_AVAILABILITY_TIME_TYPE_LOC, 'Capture time, type & location'),
    (CAPTURE_AVAILABILITY_TYPE, 'Capture type only'),
)
FEEDBACK_DISPLAY_DISABLED = "disabled"
FEEDBACK_DISPLAY_ENABLED = "enabled"
FEEDBACK_DISPLAY_CHOICES = (
    (FEEDBACK_DISPLAY_DISABLED, "Disabled"),
    (FEEDBACK_DISPLAY_ENABLED, "Enabled"),
)

FEEDBACK_DISPLAY_ITEMS = (
    ('feedback-and-judge-category', 'Judge Category and Feedback'),
    ('feedback-only', 'Only Feedback'),
    ('judge-category-only', 'Only Judge Category'))


PANEL_AVAILABILITY_KEYWORD_SLOTS = {'time': 'panel_time',
                                    'type': 'panel_type',
                                    'location': 'location'}

DEFAULT_BUFFER_BEFORE_EVENT = 30
FIFTEEN_MINUTES = 15
BUFFER_TIMES = tuple([(i * FIFTEEN_MINUTES, i * FIFTEEN_MINUTES)
                      for i in range(9)])


class JudgingRound(MCModel):
    program = models.ForeignKey(Program)
    name = models.CharField(max_length=60)
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    round_type = models.CharField(
        choices=JUDGING_ROUND_TYPE_ENUM,
        max_length=10)
    application_type = models.ForeignKey(
        ApplicationType,
        blank=True,
        null=True)
    buffer_before_event = models.IntegerField(
        choices=BUFFER_TIMES,
        default=30,
        help_text="Choose a time in increments of 15 minutes.")
    judging_form = models.ForeignKey("JudgingForm", blank=True, null=True)
    recruit_judges = models.CharField(
        max_length=16,
        choices=RECRUIT_JUDGES_ENUM,
        default=RECRUIT_NONE)
    recruiting_prompt = models.TextField(
        blank=True,
        help_text="You may use HTML, including links")
    positive_recruiting_prompt = models.TextField(
        'Positive Recruiting Response Label',
        blank=True,
        help_text="You may use HTML, including links")
    negative_recruiting_prompt = models.TextField(
        'Negative Recruiting Response Label',
        blank=True,
        help_text="You may use HTML, including links")
    capture_capacity = models.BooleanField(default=False)
    capacity_prompt = models.TextField(
        blank=True,
        help_text="You may use HTML, including links")
    capacity_options = models.CharField(
        max_length=255,
        blank=True,
        help_text="Provide a list of integers, separated by '|' "
        "(like 10|20|30)")
    capture_availability = models.CharField(
        max_length=32,
        choices=CAPTURE_AVAILABILITY_CHOICES,
        default=CAPTURE_AVAILABILITY_DISABLED)
    feedback_display = models.CharField(
        choices=FEEDBACK_DISPLAY_CHOICES,
        default=FEEDBACK_DISPLAY_DISABLED,
        max_length=10)
    feedback_merge_with = models.ForeignKey(
        'JudgingRound',
        blank=True,
        null=True,
        help_text="Optional: merge the display of this feedback with "
        "another round")
    feedback_display_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links (not relevant if "
        "merged with another round)")
    feedback_display_items = models.CharField(
        max_length=64,
        blank=True,
        choices=FEEDBACK_DISPLAY_ITEMS,
        help_text="Not relevant if merged with another round")
    judge_instructions = models.TextField(
        blank=True,
        help_text="Instructions to present to judges in this round on their "
        "judging portal.")
    presentation_mins = models.IntegerField(
        blank=True,
        default=20,
        help_text='Duration of startup pitch to judges, in minutes')
    buffer_mins = models.IntegerField(
        blank=True,
        default=10,
        help_text='Time between startup pitches, in minutes')
    break_mins = models.IntegerField(
        blank=True,
        default=10,
        help_text="Duration of judges' coffee break(s), in minutes")
    num_breaks = models.IntegerField(
        blank=True,
        default=1,
        help_text=("Number of breaks the judges will be given "
                   "during a judging panel"))
    startup_label = models.ForeignKey(
        StartupLabel,
        blank=True,
        null=True,
        help_text="Label for Startups")
    desired_judge_label = models.ForeignKey(
        UserLabel,
        blank=True,
        null=True,
        help_text="Label for Desired Judges",
        related_name="rounds_desired_for")
    confirmed_judge_label = models.ForeignKey(
        UserLabel,
        blank=True,
        null=True,
        help_text="Label for Confirmed Judges",
        related_name="rounds_confirmed_for")

    if HAS_MANAGER:
        objects = JudgingRoundManager()

    class Meta(MCModel.Meta):
        db_table = 'mc_judginground'
        managed = is_managed(db_table)
        unique_together = ('program', 'name')
        ordering = ['program__program_status',
                    '-program__end_date',
                    '-end_date_time',
                    'name']
        verbose_name_plural = 'Judging Rounds'

    def __str__(self):
        return "%s in %s" % (self.name, self.program)
