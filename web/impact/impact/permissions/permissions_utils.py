# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import logging
from django.contrib.auth import get_user_model
from mc.models import Clearance
from accelerator_abstract.models.base_clearance import (
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    CLEARANCE_LOGGER_FAILED_INSUFFICIENT_CLEARANCE_MSG,
    CLEARANCE_LOGGER_SUCCESS_MSG,
)

logger = logging.getLogger(__file__)
User = get_user_model()

# FIXME: function definitions duplicated from mc.permission_checks


def _log_access_attempt(cleared, user, level, program_family):
    if cleared:
        _log_sufficient_clearance(level, program_family, user)
    else:
        _log_insufficient_clearance(level, program_family, user)


def _log_sufficient_clearance(level, program_family, user):
    logger.info(CLEARANCE_LOGGER_SUCCESS_MSG.format(
        user=user, program_family=program_family, level=level))


def _log_insufficient_clearance(level, program_family, user):
    logger.info(CLEARANCE_LOGGER_FAILED_INSUFFICIENT_CLEARANCE_MSG.format(
        user=user, program_family=program_family, level=level))

# end duplicated definitions


def global_operations_manager_check(user, program_family=None):
    cleared = Clearance.objects.check_clearance(
        user, CLEARANCE_LEVEL_GLOBAL_MANAGER, program_family)
    _log_access_attempt(cleared, user,
                        CLEARANCE_LEVEL_GLOBAL_MANAGER, program_family)
    return cleared
