# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-
from pytz import utc
from datetime import (
    datetime,
    timedelta,
)

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from accelerator.models import (
    BucketState,
    STALE_NOSTARTUP_BUCKET_TYPE,
)

from .program_cycle_factory import ProgramCycleFactory
from .program_role_factory import ProgramRoleFactory


class BucketStateFactory(DjangoModelFactory):
    class Meta:
        model = BucketState

    name = STALE_NOSTARTUP_BUCKET_TYPE
    group = "Stale Lead Buckets"
    sort_order = 1
    cycle = SubFactory(ProgramCycleFactory)
    last_update = utc.localize(datetime.now() - timedelta(1))
    program_role = SubFactory(ProgramRoleFactory)
