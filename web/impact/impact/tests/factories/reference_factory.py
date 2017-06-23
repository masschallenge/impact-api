# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from pytz import utc
from datetime import datetime
from factory import (
    DjangoModelFactory,
    Iterator,
    Sequence,
    SubFactory,
)

from impact.models import Reference

from .application_factory import ApplicationFactory
from .entrepreneur_factory import EntrepreneurFactory


class ReferenceFactory(DjangoModelFactory):

    class Meta:
        model = Reference

    application = SubFactory(ApplicationFactory)
    email = Sequence(lambda n: "test_email{0}@example.com".format(n))
    first_name = Sequence(lambda n: "name{0}".format(n))
    last_name = Sequence(lambda n: "name{0}".format(n))
    title = Sequence(lambda n: "title{0}".format(n))
    company = Sequence(lambda n: "company{0}".format(n))
    reference_hash = Sequence(lambda n: "reference_hash{0}".format(n))
    sent = utc.localize(datetime(2015, 10, 1, 12))
    accessed = utc.localize(datetime(2015, 11, 1, 12))
    submitted = utc.localize(datetime(2015, 12, 2, 12))
    confirmed_first_name = Sequence(lambda n: "User_First{0}".format(n))
    confirmed_last_name = Sequence(lambda n: "User_Last{0}".format(n))
    confirmed_company = Sequence(lambda n: "Company{0}".format(n))
    question_1_rating = Iterator([1, 2, 3, 4])
    question_2_rating = Iterator([1, 2, 3, 4, 5])
    comments = "This is the best startup ever."
    requesting_user = SubFactory(EntrepreneurFactory)
