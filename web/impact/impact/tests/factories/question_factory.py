# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)
from impact.models import (
    CHOICE_LAYOUT_HORIZONTAL,
    Question,
    QUESTION_TYPE_MULTILINE,
)


class QuestionFactory(DjangoModelFactory):

    class Meta:
        model = Question

    name = Sequence(lambda n: "Question {0}".format(n))
    question_type = QUESTION_TYPE_MULTILINE
    choice_options = ""
    choice_layout = CHOICE_LAYOUT_HORIZONTAL
