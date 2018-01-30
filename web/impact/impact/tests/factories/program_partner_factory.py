# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import ProgramPartner

from .partner_factory import PartnerFactory
from .program_factory import ProgramFactory
from .program_partner_type_factory import ProgramPartnerTypeFactory


class ProgramPartnerFactory(DjangoModelFactory):

    class Meta:
        model = ProgramPartner

    program = SubFactory(ProgramFactory)
    partner = SubFactory(PartnerFactory)
    partner_type = SubFactory(ProgramPartnerTypeFactory)
    description = Sequence(
        lambda n: "Description of Program Partner #{0}".format(n))
