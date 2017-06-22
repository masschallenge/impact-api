# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)

from impact.models import FunctionalExpertise


class FunctionalExpertiseFactory(DjangoModelFactory):

    class Meta:
        model = FunctionalExpertise

    name = Sequence(lambda n: "Functional Expertise {0}".format(n))
    lft = 0
    rght = 0
    tree_id = 0
    level = 0

    # DO NOT provide a slot for parent.  The parent slot appears to get
    # handled correctly by MPTT and if you try to override
    # it, then you end up having to move a node between trees
    # which apparent MPTT does not support.
