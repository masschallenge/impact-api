# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)
from accelerator.models import PartnerTeamMember

from .partner_factory import PartnerFactory
from .entrepreneur_factory import EntrepreneurFactory


class PartnerTeamMemberFactory(DjangoModelFactory):

    class Meta:
        model = PartnerTeamMember

    partner = SubFactory(PartnerFactory)
    team_member = SubFactory(EntrepreneurFactory)
    partner_administrator = False
