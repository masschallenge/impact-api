# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from django.core.validators import (
    RegexValidator,
    validate_slug
)

try:
    from sorl.thumbnail import ImageField
    HAS_SORL = True
except ImportError:
    HAS_SORL = False

from impact.models.mc_model import MCModel
from impact.models.organization import Organization
from impact.models.utils import is_managed


class Partner(MCModel):
    name = models.CharField(max_length=100, unique=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)    
    description = models.TextField(
        max_length=1000,
        blank=True,
        help_text='This is the generic description of the Partner, shared '
        'across all Programs.')
    if HAS_SORL:
        partner_logo = ImageField(
            upload_to='startup_pics',
            verbose_name="Partner Logo",
            blank=True)
    else:
        partner_logo = models.CharField(max_length=100)

    website_url = models.URLField(max_length=100, blank=True)
    twitter_handle = models.CharField(
        max_length=40,
        blank=True,
        help_text='Omit the "@". We\'ll add it.')
    public_inquiry_email = models.EmailField(verbose_name="Email address",
                                             max_length=100,
                                             blank=True)
    url_slug = models.CharField(
        max_length=64,
        blank=True,
        default="",  # This actually gets replaced by a real slug.
        unique=True,
        validators=[RegexValidator(".*\D.*",
                                   "Slug must contain a non-numeral."),
                    validate_slug, ]
    )

    class Meta(MCModel.Meta):
        db_table = 'mc_partner'
        managed = is_managed(db_table)
        verbose_name_plural = 'Partners'
        ordering = ['name', ]

    def __str__(self):
        return self.name
