# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.application import Application
from impact.models.mc_model import MCModel
from impact.models.judging_form import JudgingForm
from impact.models.judge_application_feedback_manager import (
    JudgeApplicationFeedbackManager,
)
from impact.models.panel import Panel
from impact.models.utils import is_managed

import logging

logger = logging.getLogger(__file__)


JUDGING_FEEDBACK_STATUS_COMPLETE = "COMPLETE"
JUDGING_FEEDBACK_STATUS_INCOMPLETE = "INCOMPLETE"
JUDGING_FEEDBACK_STATUS_CONFLICT = "NOT-JUDGED-CONFLICT"
JUDGING_FEEDBACK_STATUS_OTHER = "NOT-JUDGED-OTHER"
JUDGING_FEEDBACK_STATUS_ENUM = (
    (JUDGING_FEEDBACK_STATUS_COMPLETE, 'COMPLETE'),
    (JUDGING_FEEDBACK_STATUS_INCOMPLETE, 'INCOMPLETE'),
    (JUDGING_FEEDBACK_STATUS_CONFLICT, 'NOT JUDGED, CONFLICT'),
    (JUDGING_FEEDBACK_STATUS_OTHER, 'NOT JUDGED, OTHER'), )


JUDGING_STATUS_NO_CONFLICT = 1
JUDGING_STATUS_CONFLICT = 2
JUDGING_STATUS_OTHER = 3
JUDGING_STATUS_ENUM = (
    (JUDGING_STATUS_NO_CONFLICT, 'No Conflict'),
    (JUDGING_STATUS_CONFLICT, 'Not Judged - Conflict of Interest'),
    (JUDGING_STATUS_OTHER, 'Not Judged - Other (eg., no show)'), )


class JudgeApplicationFeedback(MCModel):
    application = models.ForeignKey(Application)
    form_type = models.ForeignKey(JudgingForm)
    judge = models.ForeignKey(settings.AUTH_USER_MODEL)
    panel = models.ForeignKey(Panel)
    judging_status = models.IntegerField(
        null=True,
        blank=True,
        choices=JUDGING_STATUS_ENUM)
    feedback_status = models.CharField(
        max_length=20,
        editable=False,
        choices=JUDGING_FEEDBACK_STATUS_ENUM)

    objects = JudgeApplicationFeedbackManager()

    class Meta(MCModel.Meta):
        db_table = 'accelerator_judgeapplicationfeedback'
        managed = is_managed(db_table)
        verbose_name_plural = 'Judge Application Feedback'
        unique_together = ('application', 'judge', 'panel')

    def __str__(self):
        return 'Feedback to Application %s by Judge %s' % (self.application,
                                                           self.judge)
