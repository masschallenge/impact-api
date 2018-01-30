# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)
from accelerator.models import UserRole


class UserRoleFactory(DjangoModelFactory):

    class Meta:
        model = UserRole

    name = Sequence(lambda n: "User Role {0}".format(n))
    url_slug = Sequence(lambda n: "role_{0}".format(n))
    sort_order = Sequence(lambda n: n)
