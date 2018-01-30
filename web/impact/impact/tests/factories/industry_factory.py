# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
)

from accelerator.models import Industry


class IndustryFactory(DjangoModelFactory):

    class Meta:
        model = Industry

    name = Sequence(lambda n: "Industry {0}".format(n))
    icon = Sequence(lambda n: "path_to_icon_{0}".format(n))
    lft = 0
    rght = 0
    tree_id = 0
    level = 0

    # DO NOT provide a slot for parent.  The parent slot appears to get
    # handled correctly by MPTT and if you try to override
    # it, then you end up having to move a node between trees
    # which apparent MPTT does not support.
