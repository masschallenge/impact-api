# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from mc.models import Industry
from .mptt_model_helper import MPTTModelHelper


class IndustryHelper(MPTTModelHelper):
    model = Industry
