# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from factory import (
    DjangoModelFactory
)
from accelerator.models import Currency


class CurrencyFactory(DjangoModelFactory):

    class Meta:
        model = Currency
