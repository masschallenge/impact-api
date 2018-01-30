# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from accelerator.models import ProgramRoleGrant

from .member_factory import MemberFactory
from .program_role_factory import ProgramRoleFactory


class ProgramRoleGrantFactory(DjangoModelFactory):

    class Meta:
        model = ProgramRoleGrant

    person = SubFactory(MemberFactory)
    program_role = SubFactory(ProgramRoleFactory)
