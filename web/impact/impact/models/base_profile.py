# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.conf import settings
from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed

BASE_ENTREPRENEUR_TYPE = "ENTREPRENEUR"
BASE_EXPERT_TYPE = "EXPERT"
BASE_MEMBER_TYPE = "MEMBER"

USER_TYPES = ((BASE_EXPERT_TYPE, 'Expert'),
              (BASE_ENTREPRENEUR_TYPE, 'Entrepreneur'),
              (BASE_MEMBER_TYPE, 'Member'))

TWITTER_HANDLE_MAX_LENGTH = 16
PHONE_MAX_LENGTH = 20


class BaseProfile(MCModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    user_type = models.CharField(max_length=16, choices=USER_TYPES)
    privacy_policy_accepted = models.BooleanField(
        default=False,
        blank=False,
        null=False)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_baseprofile'
        managed = is_managed(db_table)

    def __str__(self):
        fn = self.user.first_name
        ln = self.user.last_name
        if fn and ln:
            identifier = "%s %s" % (fn, ln)
        else:
            identifier = self.user.email
        return "Base Profile for %s" % identifier
