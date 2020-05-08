# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import Industry
from .v1.helpers.mptt_model_helper import MPTTModelHelper


class IndustryHelper(MPTTModelHelper):
    model = Industry
