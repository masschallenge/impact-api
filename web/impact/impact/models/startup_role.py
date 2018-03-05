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
    WINNER = "Winner"
    GOLD_WINNER = "Gold Winner"
    SILVER_WINNER = "Silver Winner"
    PLATINUM_WINNER = "Platinum Winner"
    DIAMOND_WINNER = "Diamond Winner"
    INKIND_WINNER = "In-Kind Winner"
    SIDECAR_WINNER = "Sidecar Winner"

    FINALIST_STARTUP_ROLES = [FINALIST,
                              AIR,
                              MC_STAFF]

    WINNER_STARTUP_ROLES = [WINNER,
                            GOLD_WINNER,
                            SILVER_WINNER,
                            PLATINUM_WINNER,
                            DIAMOND_WINNER,
                            INKIND_WINNER,
                            SILVER_WINNER]

    name = CharField(max_length=255)

    class Meta(MCModel.Meta):
        db_table = 'mc_startuprole'
        managed = is_managed(db_table)

    def __str__(self):
        return self.name
