# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import ProgramRole

from .program_factory import ProgramFactory
from .user_role_factory import UserRoleFactory
from .user_label_factory import UserLabelFactory


class ProgramRoleFactory(DjangoModelFactory):

    class Meta:
        model = ProgramRole

    program = SubFactory(ProgramFactory)
    name = Sequence(lambda n: "Program Role {0}".format(n))
    user_role = SubFactory(UserRoleFactory)
    user_label = SubFactory(UserLabelFactory)
    landing_page = None
