# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from accelerator.models import Partner
from .organization_factory import OrganizationFactory


class PartnerFactory(DjangoModelFactory):

    class Meta:
        model = Partner

    description = Sequence(lambda n: "Description of Partner {0}".format(n))
    organization = SubFactory(OrganizationFactory)
    partner_logo = Sequence(lambda n: "logo {0}".format(n))
