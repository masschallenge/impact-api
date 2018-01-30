# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from accelerator.models import ProgramPartnerType


class ProgramPartnerTypeFactory(DjangoModelFactory):

    class Meta:
        model = ProgramPartnerType

    partner_type = Sequence(lambda n: 'Test Partner Type %d' % n)
    program = SubFactory("mc.tests.factories.DefaultProgramFactory")
    description = Sequence(
        lambda n: "Description of Program Partner Type #{0}".format(n))
    feature_in_footer = False
    sort_order = 1
    badge_image = None
    badge_display = "NONE"
