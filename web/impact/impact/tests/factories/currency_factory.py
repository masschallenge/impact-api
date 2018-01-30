# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)

from accelerator.models.currency import Currency


def _char_range(start, end):
    return [chr(i) for i in range(ord(start), ord(end) + 1)]


ABBR_CHARS = (_char_range('a', 'z') +
              _char_range('0', '9'))


def nth_currency(index):
    count = len(ABBR_CHARS)
    index1 = int(index % count)
    remainder = index / count
    index2 = int(remainder % count)
    remainder = remainder / count
    index3 = int(remainder % count)
    return ABBR_CHARS[index1] + ABBR_CHARS[index2] + ABBR_CHARS[index3]


class CurrencyFactory(DjangoModelFactory):
    class Meta:
        model = Currency

    name = Sequence(lambda n: "Currency {0}".format(n))
    abbr = Sequence(lambda n: nth_currency(n))
    usd_exchange = 1.0
