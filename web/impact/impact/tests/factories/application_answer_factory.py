# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import ApplicationAnswer

from .application_factory import ApplicationFactory
from .application_question_factory import ApplicationQuestionFactory


class ApplicationAnswerFactory(DjangoModelFactory):

    class Meta:
        model = ApplicationAnswer

    application = SubFactory(ApplicationFactory)
    application_question = SubFactory(ApplicationQuestionFactory)
    answer_text = Sequence(lambda n: "Answer Text {0}".format(n))
