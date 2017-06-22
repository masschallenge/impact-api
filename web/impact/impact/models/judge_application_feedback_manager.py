# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models


class JudgeApplicationFeedbackManager(models.Manager):

    """custom table-level methods for this model"""

    def for_assignment(self, assignment):
        return self.get_queryset().filter(
            judge=assignment.judge.id,
            panel=assignment.panel.id,
        )

    def get_feedbacks_status(self, assignment):
        """used by mc_judge.views.PanelReportView"""
        qs = self.for_assignment(assignment)
        completed = qs.filter(
            feedback_status__in=[
                'COMPLETE', 'NOT-JUDGED-CONFLICT', 'NOT-JUDGED-OTHER',
            ]
        ).count()
        has_incomplete = qs.filter(
            feedback_status='INCOMPLETE'
        ).exists()
        return completed, has_incomplete
