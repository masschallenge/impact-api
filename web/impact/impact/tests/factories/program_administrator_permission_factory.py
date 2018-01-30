# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)
from accelerator.models import ProgramAdministratorPermission
from .program_factory import ProgramFactory


class ProgramAdministratorPermissionFactory(DjangoModelFactory):
    class Meta:
        model = ProgramAdministratorPermission

    permission = 'view'
    model = 'judgepanelassignment'
    description = ''
    program = SubFactory(ProgramFactory)
