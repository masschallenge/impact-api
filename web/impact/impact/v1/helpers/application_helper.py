# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import Application
from impact.v1.helpers.mptt_model_helper import MPTTModelHelper


class ApplicationHelper(MPTTModelHelper):
    model = Application
