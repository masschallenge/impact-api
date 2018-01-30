# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models import ApplicationQuestion
from impact.models.utils import is_managed


class ApplicationAnswer(MCModel):
    application = models.ForeignKey("Application")
    application_question = models.ForeignKey(ApplicationQuestion)
    answer_text = models.CharField(max_length=2000, blank=True)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_applicationanswer'
        managed = is_managed(db_table)
        verbose_name_plural = 'Application Answers'

    def __str__(self):
        return "Answer to question %s from %s" % (
            self.application_question.question_number,
            self.application.startup.name)
