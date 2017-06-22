# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from simpleuser.models import User
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


ACTIVE_PANEL_STATUS = "ACTIVE"
COMPLETED_PANEL_STATUS = "COMPLETED"
DEFAULT_PANEL_STATUS = "NOT STARTED"
PREVIEW_PANEL_STATUS = "PREVIEW"
PANEL_STATUS_ENUM = ((DEFAULT_PANEL_STATUS, "NOT STARTED"),
                     (PREVIEW_PANEL_STATUS, "PREVIEW"),
                     (ACTIVE_PANEL_STATUS, "ACTIVE"),
                     (COMPLETED_PANEL_STATUS, "COMPLETED"), )


class Panel(MCModel):
    judges = models.ManyToManyField(
        User,
        related_name="panels",
        through="impact.JudgePanelAssignment")
    applications = models.ManyToManyField(
        'Application',
        related_name='panels',
        through="impact.ApplicationPanelAssignment")
    panel_time = models.ForeignKey('PanelTime', blank=True, null=True)
    panel_type = models.ForeignKey('PanelType', blank=True, null=True)
    description = models.CharField(max_length=30, blank=True)
    location = models.ForeignKey('PanelLocation', blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=PANEL_STATUS_ENUM,
        default='NOT STARTED')

    class Meta(MCModel.Meta):
        db_table = 'mc_panel'
        managed = is_managed(db_table)
        verbose_name_plural = 'Panels'

    def __str__(self):
        if self.description:
            return self.description
        else:
            if self.panel_type and self.panel_time:
                return "%s panel: %s (ID %s)" % (self.panel_type,
                                                 self.panel_time,
                                                 self.pk)
            else:
                return "Panel %s" % self.pk
