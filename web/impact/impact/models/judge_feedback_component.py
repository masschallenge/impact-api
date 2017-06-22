# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.judge_application_feedback import JudgeApplicationFeedback
from impact.models.judging_form_element import JudgingFormElement
from impact.models.utils import is_managed


JUDGE_FEEDBACK_REVIEWER = "_RESTRICTED_: Judge Feedback Reviewer"
JUDGE_FEEDBACK_SANITIZER = "_CAUTION_: Judge Feedback Sanitizer"


class JudgeFeedbackComponent(MCModel):
    judge_feedback = models.ForeignKey(JudgeApplicationFeedback)
    feedback_element = models.ForeignKey(JudgingFormElement)
    answer_text = models.CharField(max_length=2000, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_judgefeedbackcomponent'
        managed = is_managed(db_table)
        verbose_name_plural = 'Feedback Components'
        unique_together = ('judge_feedback', 'feedback_element')

    def __str__(self):
        return "Feedback for component %s from %s" % (
            self.feedback_element.element_number,
            self.judge_feedback.judge)
