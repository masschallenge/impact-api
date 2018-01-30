# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)

from accelerator.models import MentoringSpecialties


class MentoringSpecialtiesFactory(DjangoModelFactory):

    class Meta:
        model = MentoringSpecialties

    name = Sequence(lambda n: "Mentoring Specialties {0}".format(n))
