# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# -*- coding: utf-8 -*-

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)

from accelerator.models import (
    PREVIEW_PANEL_STATUS,
    Panel,
)

from .panel_location_factory import PanelLocationFactory
from .panel_time_factory import PanelTimeFactory
from .panel_type_factory import PanelTypeFactory


class PanelFactory(DjangoModelFactory):

    class Meta:
        model = Panel

    panel_time = SubFactory(PanelTimeFactory)
    panel_type = SubFactory(PanelTypeFactory)
    description = Sequence(lambda n: "Panel Description {0}".format(n))
    location = SubFactory(PanelLocationFactory)
    status = PREVIEW_PANEL_STATUS
