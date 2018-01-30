# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from decimal import Decimal
from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import (
    ACTIVE_PROGRAM_STATUS,
    Program,
)
from impact.tests.utils import months_from_now

from .program_family_factory import ProgramFamilyFactory
from .program_cycle_factory import ProgramCycleFactory


class ProgramFactory(DjangoModelFactory):
    class Meta:
        model = Program

    name = Sequence(lambda n: "Name of Program {0}".format(n))
    program_family = SubFactory(ProgramFamilyFactory)
    cycle = SubFactory(ProgramCycleFactory)
    description = Sequence(lambda n: "Description for Program {0}".format(n))
    start_date = months_from_now(-2)
    end_date = months_from_now(2)
    location = Sequence(
        lambda n: "Location Program {0}".format(n))
    program_status = ACTIVE_PROGRAM_STATUS
    currency_code = "USD"
    early_application_fee = Decimal(49.00)
    regular_application_fee = Decimal(99.00)
    regular_fee_suffix = ""
    interested_judge_message = Sequence(
        lambda n: "Interested Judge Program {0}".format(n))
    approved_judge_message = Sequence(
        lambda n: "Approved Judge Program {0}".format(n))
    interested_mentor_message = Sequence(
        lambda n: "Interested Mentor Program {0}".format(n))
    approved_mentor_message = Sequence(
        lambda n: "Approved Mentor Program {0}".format(n))
    interested_speaker_message = Sequence(
        lambda n: "Interested Speaker Program {0}".format(n))
    approved_speaker_message = Sequence(
        lambda n: "Approved Speaker Program {0}".format(n))
    interested_office_hours_message = Sequence(
        lambda n: "Interested Office Hours Program {0}".format(n))
    approved_office_hours_message = Sequence(
        lambda n: "Approved Office Hours Program {0}".format(n))
    refund_code_support = "enabled"
    many_codes_per_partner = False
    url_slug = Sequence(lambda n: "p{0}".format(n))
    mentor_program_group = None
    overview_start_date = None
    overview_deadline_date = None
