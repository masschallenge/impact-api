# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.named_group import NamedGroup
from impact.models.program_family import ProgramFamily
from impact.models.program_manager import ProgramManager
from impact.models.program_cycle import ProgramCycle
from impact.models.utils import is_managed

ACTIVE_PROGRAM_STATUS = "active"
ENDED_PROGRAM_STATUS = "ended"
HIDDEN_PROGRAM_STATUS = "hidden"
UPCOMING_PROGRAM_STATUS = "upcoming"
PROGRAM_STATUSES = ((UPCOMING_PROGRAM_STATUS, 'Upcoming'),
                    (ACTIVE_PROGRAM_STATUS, 'Active'),
                    (ENDED_PROGRAM_STATUS, 'Ended'),
                    (HIDDEN_PROGRAM_STATUS, 'Hidden'))
CURRENT_STATUSES = [ACTIVE_PROGRAM_STATUS, UPCOMING_PROGRAM_STATUS]

REFUND_CODES_DISABLED = "disabled"
REFUND_CODES_ENABLED = "enabled"
REFUND_CODES_VIEW_ONLY = "view-submitted-only"

REFUND_CODE_SUPPORT_VALUES = (
    (REFUND_CODES_ENABLED, "Enabled"),
    (REFUND_CODES_VIEW_ONLY, "View Submitted Only"),
    (REFUND_CODES_DISABLED, "Disabled"),
)


class Program(MCModel):
    """a masschallenge program"""

    objects = ProgramManager()

    name = models.CharField(max_length=50)
    program_family = models.ForeignKey(
        ProgramFamily,
        blank=True,
        null=True,
        related_name="programs",
    )
    cycle = models.ForeignKey(
        ProgramCycle,
        blank=True,
        null=True,
        related_name="programs")
    description = models.CharField(max_length=500, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=50)
    program_status = models.CharField(
        max_length=64,
        choices=PROGRAM_STATUSES,
    )
    currency_code = models.CharField(max_length=3)
    early_application_fee = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    regular_application_fee = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    regular_fee_suffix = models.CharField(max_length=20, blank=True)
    interested_judge_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links"
    )
    approved_judge_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links")
    interested_mentor_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links"
    )
    approved_mentor_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links")
    interested_speaker_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links"
    )
    approved_speaker_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links")
    interested_office_hours_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links"
    )
    approved_office_hours_message = models.TextField(
        blank=True,
        help_text="You may use HTML, including links")
    refund_code_support = models.CharField(
        max_length=64,
        choices=REFUND_CODE_SUPPORT_VALUES,
        default='enabled',
    )
    many_codes_per_partner = models.BooleanField(
        default=False,
        verbose_name="Allow multiple refund codes per partner",
        help_text="If true, then a given application may apply more than one "
                  "refund code from the same partner for this program"
    )
    url_slug = models.CharField(
        max_length=30,
        default="",
    )
    mentor_program_group = models.ForeignKey(
        NamedGroup,
        blank=True,
        null=True)
    overview_start_date = models.DateTimeField(blank=True, null=True)
    overview_deadline_date = models.DateTimeField(blank=True, null=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_program'
        managed = is_managed(db_table)
        verbose_name_plural = 'Programs'
        ordering = ['-end_date', 'name']

    def __str__(self):
        return self.name

    def family_abbr(self):
        return self.program_family.url_slug.upper()
