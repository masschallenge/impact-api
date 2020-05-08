# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import FunctionalExpertise
from .mptt_model_helper import MPTTModelHelper


class FunctionalExpertiseHelper(MPTTModelHelper):
    model = FunctionalExpertise
