# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Iterator,
)
from accelerator.models import ExpertCategory

# The next import is indicative of a deeper problem with how
# ExpertCategorys are currently used.  See AC-5022 for the underlying
# issue and a discussion of possible better long term solutions.
from impact.v1.helpers.profile_helper import VALID_EXPERT_CATEGORIES


class ExpertCategoryFactory(DjangoModelFactory):

    class Meta:
        model = ExpertCategory

    name = Iterator(VALID_EXPERT_CATEGORIES)
