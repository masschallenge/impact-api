# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models
from impact.models.mc_model import MCModel

from impact.models.panel import Panel
from impact.models.judge_panel_assignment_manager import (
    JudgePanelAssignmentManager,
)
from impact.models.utils import is_managed

ASSIGNED_PANEL_ASSIGNMENT_STATUS = "ASSIGNED"
COMPLETE_PANEL_ASSIGNMENT_STATUS = "COMPLETE"

JUDGE_PANEL_ASSIGNMENT_STATUS_ENUM = (
    (ASSIGNED_PANEL_ASSIGNMENT_STATUS, ASSIGNED_PANEL_ASSIGNMENT_STATUS),
    (COMPLETE_PANEL_ASSIGNMENT_STATUS, COMPLETE_PANEL_ASSIGNMENT_STATUS)
)


class JudgePanelAssignment(MCModel):
    judge = models.ForeignKey(settings.AUTH_USER_MODEL)
    panel = models.ForeignKey(Panel)
    scenario = models.ForeignKey(
        'Scenario',
        related_name='judge_assignments')
    assignment_status = models.CharField(
        choices=JUDGE_PANEL_ASSIGNMENT_STATUS_ENUM,
        max_length=16,
        blank=True,
        default="")
    panel_sequence_number = models.PositiveIntegerField(
        help_text="Indicate in which order this panel should be completed "
        "by this judge",
        blank=True,
        null=True)

    objects = JudgePanelAssignmentManager()

    class Meta(MCModel.Meta):
        db_table = 'mc_judgepanelassignment'
        managed = is_managed(db_table)
        verbose_name_plural = "assignments of judge to panel"
        unique_together = ('judge', 'panel', 'scenario')

    def __str__(self):
        tmpl = "%s -> %s"
        return tmpl % (self.judge, self.panel)
