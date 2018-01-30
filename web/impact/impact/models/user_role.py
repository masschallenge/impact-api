# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db.models import (
    CharField,
    PositiveIntegerField,
)

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class UserRole(MCModel):
    # Known User Roles
    ACTIVE_JUDGE = "Active Judge"
    ALUM = "Alum"
    ALUM_MENTOR = "Alum Mentor"
    AIR = "Alumni in Residence"
    MENTOR = "Mentor"
    DESIRED_JUDGE = "Desired Judge"
    DESIRED_MENTOR = "Desired Mentor"
    FINALIST = "Finalist"
    JUDGE = "Judge"
    OFFICE_HOUR_HOLDER = "Office Hour Holder"
    PARTNER = "Partner"
    PARTNER_ADMIN = "Partner Admin"
    PROCTOR = "Proctor"
    SENIOR_JUDGE = "Senior Judge"
    STAFF = "Staff"
    TEAM = "Team"

    OFFICE_HOUR_ROLES = set([AIR,
                             PARTNER,
                             PARTNER_ADMIN,
                             OFFICE_HOUR_HOLDER,
                             MENTOR])

    FINALIST_USER_ROLES = [FINALIST,
                           AIR,
                           STAFF]

    name = CharField(max_length=255)
    url_slug = CharField(max_length=30)
    sort_order = PositiveIntegerField()

    class Meta(MCModel.Meta):
        db_table = 'accelerator_userrole'
        managed = is_managed(db_table)

    def __str__(self):
        return self.name
