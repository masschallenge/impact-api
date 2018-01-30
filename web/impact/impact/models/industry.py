# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

try:
    from mptt.models import (
        MPTTModel,
        TreeForeignKey
    )
    cls = MPTTModel
    HAS_MPTT = True
except:
    cls = models.Model
    HAS_MPTT = False

from impact.models.utils import is_managed


class Industry(cls):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, blank=True)
    if HAS_MPTT:
        parent = TreeForeignKey('self',
                                null=True,
                                blank=True,
                                related_name="children")

        class MPTTMeta:
            order_insertion_by = ['name', ]
            verbose_name_plural = 'Industries'

        class Meta:
            db_table = 'accelerator_industry'
            managed = is_managed(db_table)
            verbose_name_plural = "Industries"
    else:
        parent = models.ForeignKey('self', blank=True, null=True)
        lft = models.IntegerField()
        rght = models.IntegerField()
        tree_id = models.IntegerField()
        level = models.IntegerField()

        class Meta:
            db_table = 'accelerator_industry'
            managed = is_managed(db_table)
            verbose_name_plural = "Industries"

    def __str__(self):
        parent_name = ''
        if self.parent:
            parent_name = "%s - " % self.parent.name
        return "%s%s" % (parent_name, self.name)
