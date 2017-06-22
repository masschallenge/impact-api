# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.panel import Panel
from impact.models.utils import is_managed


class ApplicationPanelAssignment(MCModel):
    application = models.ForeignKey("Application")
    panel = models.ForeignKey(Panel)
    scenario = models.ForeignKey(
        'Scenario',
        related_name='application_assignments'
    )
    panel_slot_number = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True)
    remote_pitch = models.BooleanField(default=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_applicationpanelassignment'
        managed = is_managed(db_table)
        verbose_name_plural = "assignments of startup applications to panel"
        unique_together = ('application', 'panel', 'scenario')
        ordering = ['panel_slot_number']

    def __str__(self):
        tmpl = "%s -> %s"
        return tmpl % (self.application, self.panel)
