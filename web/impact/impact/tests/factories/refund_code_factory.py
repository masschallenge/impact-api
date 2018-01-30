# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    post_generation,
    Sequence,
    SubFactory,
)

from accelerator.models import RefundCode

from .partner_factory import PartnerFactory


class RefundCodeFactory(DjangoModelFactory):

    class Meta:
        model = RefundCode

    unique_code = Sequence(lambda n: "test_code{0}".format(n))
    issued_to = SubFactory(PartnerFactory)
    discount = 50
    maximum_uses = 1
    notes = "Notes about this refund code"
    internal = False

    @post_generation
    def programs(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for program in extracted:
                self.programs.add(program)
