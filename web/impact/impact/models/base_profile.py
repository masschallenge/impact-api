# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from simpleuser.models import User

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


USER_TYPES = (('EXPERT', 'Expert'),
              ('ENTREPRENEUR', 'Entrepreneur'),
              ('MEMBER', 'Member'))


class BaseProfile(MCModel):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=16, choices=USER_TYPES)
    privacy_policy_accepted = models.BooleanField(
        default=False,
        blank=False,
        null=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_baseprofile'
        managed = is_managed(db_table)

    def __str__(self):
        fn = self.user.first_name
        ln = self.user.last_name
        if fn and ln:
            identifier = "%s %s" % (fn, ln)
        else:
            identifier = self.user.username
        return "Base Profile for %s" % identifier
