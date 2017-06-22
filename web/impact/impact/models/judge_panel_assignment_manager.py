# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models


class JudgePanelAssignmentManager(models.Manager):

    """custom table-level methods for the JudgePanelAssignment model"""

    def get_panel_assignments(self, panels):
        qs = self.get_queryset().filter(
            panel__in=panels, scenario__is_active=True
        ).order_by('panel', 'judge__last_name')
        return qs
