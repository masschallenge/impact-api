# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db import models

from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class Currency(MCModel):
    name = models.CharField(max_length=64, unique=True)
    abbr = models.CharField(max_length=3, unique=True)
    usd_exchange = models.FloatField()

    class Meta(MCModel.Meta):
        db_table = 'mc_currency'
        managed = is_managed(db_table)

    def __str__(self):
        return self.name

    @classmethod
    def choices(cls):
        return [(c["id"], c["name"])
                for c in cls.objects.all().values("id", "name")]

    @classmethod
    def default_currency(cls):
        usd = cls.objects.filter(abbr="USD")
        if usd:
            return usd[0]
        return cls.objects.all()[0]
