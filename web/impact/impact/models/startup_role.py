# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db.models import CharField

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class StartupRole(MCModel):
    # Known Startup Roles
    FINALIST = "Finalist"
    ENTRANT = "Entrant"
    FAST_TRACK = "Fast Track"
    AIR = "Alum In Residence"
    MC_STAFF = "MC Staff"

    FINALIST_STARTUP_ROLES = [FINALIST,
                              AIR,
                              MC_STAFF]

    name = CharField(max_length=255)

    class Meta(MCModel.Meta):
        db_table = 'accelerator_startuprole'
        managed = is_managed(db_table)

    def __str__(self):
        return self.name
