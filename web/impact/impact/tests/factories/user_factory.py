# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)

from django.contrib.auth.hashers import make_password
from simpleuser.models import User


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    email = Sequence(lambda n: "user_{0}@example.com".format(n))
    full_name = Sequence(lambda n: "First {0}".format(n))
    short_name = Sequence(lambda n: "Last {0}".format(n))
    is_superuser = False
    is_staff = False
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        # Hash the password if it has been provided
        if 'password' in kwargs:
            kwargs['password'] = make_password(kwargs['password'])
        else:
            kwargs['password'] = make_password('password!')

        return super()._prepare(create, **kwargs)
