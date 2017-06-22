# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)
from impact.models import Partner


class PartnerFactory(DjangoModelFactory):

    class Meta:
        model = Partner

    name = Sequence(lambda n: "Test Partner {0}".format(n))
    description = Sequence(lambda n: "Description of Partner {0}".format(n))
    partner_logo = None
    website_url = Sequence(lambda n: "www.partner{0}.com".format(n))
    twitter_handle = Sequence(lambda n: "partner{0}".format(n))
    public_inquiry_email = Sequence(
        lambda n: "contact@partner{0}.com".format(n))
    url_slug = ""
