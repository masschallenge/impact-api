# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class RecommendationTag(MCModel):

    """
    Tag model used for storing keywords for a particular model.
    This is also fed into the recommendation engine.
    """
    text = models.TextField()

    class Meta(MCModel.Meta):
        db_table = 'accelerator_recommendationtag'
        managed = is_managed(db_table)
        pass
