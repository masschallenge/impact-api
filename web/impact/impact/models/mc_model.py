# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models


class MCModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta(object):
        abstract = True
