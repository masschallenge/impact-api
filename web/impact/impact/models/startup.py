# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from embed_video.fields import EmbedVideoField

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

try:
    from sorl.thumbnail import ImageField
    HAS_SORL = True  # pragma: no cover
except ImportError:  # pragma: no cover - handle in AC-4750
    HAS_SORL = False  # pragma: no cover

from accelerator.models.currency import Currency
from impact.models.mc_model import MCModel
from impact.models.organization import Organization
from impact.models.industry import Industry
from impact.models.recommendation_tag import RecommendationTag
from impact.models.utils import is_managed

import logging

logger = logging.getLogger(__name__)

DEFAULT_PROFILE_BACKGROUND_COLOR = "217181"  # default dark blue

DEFAULT_PROFILE_TEXT_COLOR = "FFFFFF"

STARTUP_COMMUNITIES = (
    ("red", "Red"),
    ("blue", "Blue"),
    ("green", "Green"),
)


class Startup(MCModel):
    organization = models.ForeignKey(Organization, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_visible = models.BooleanField(
        default=True,
        help_text="Public Profiles will be published on the MassChallenge web "
                  "site. Stealth profiles will only be shared with judges.",
    )
    primary_industry = models.ForeignKey(
        Industry,
        verbose_name="Primary Industry",
        related_name="startups")
    additional_industries = models.ManyToManyField(
        Industry,
        verbose_name="Additional Industries",
        related_name="secondary_startups",
        db_table="mc_startup_related_industry",
        blank=True,
        help_text="You may select up to 5 related industries.",
    )
    short_pitch = models.CharField(
        max_length=140,
        blank=False,
        help_text="Your startup in 140 characters or less.")
    full_elevator_pitch = models.TextField(
        max_length=500,
        blank=False,
        help_text="Your startup in 500 characters or less.")
    linked_in_url = models.URLField(max_length=100, blank=True)
    facebook_url = models.URLField(max_length=100, blank=True)

    if HAS_SORL:
        high_resolution_logo = ImageField(
            upload_to="startup_pics",
            verbose_name="High Resolution Logo",
            blank=True)  # pragma: no cover
    else:
        high_resolution_logo = models.CharField(max_length=100,
                                                null=True)  # pragma: no cover

    video_elevator_pitch_url = EmbedVideoField(
        max_length=100,
        blank=True,
        help_text=(
            "The Startup Profile video is great way to show off your "
            "startup to the judges and the broader MassChallenge "
            "community (if you're not in stealth mode). Brevity is "
            "recommended and videos should not be longer than 1-3 "
            "minutes. Please submit YouTube or Vimeo URLs.")
    )

    created_datetime = models.DateTimeField(blank=True, null=True)
    last_updated_datetime = models.DateTimeField(blank=True, null=True)
    community = models.CharField(
        max_length=64,
        choices=STARTUP_COMMUNITIES,
        blank=True,
    )

    # profile color fields are deprecated - do not delete until we know
    # what the marketing site is doing with startup display

    profile_background_color = models.CharField(
        max_length=7,
        blank=True,
        default=DEFAULT_PROFILE_BACKGROUND_COLOR,
        validators=[RegexValidator(
            "^([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|)$",
            "Color must be 3 or 6-digit hexecimal number, "
            "such as FF0000 for red."), ]
    )
    profile_text_color = models.CharField(
        max_length=7,
        blank=True,
        default=DEFAULT_PROFILE_TEXT_COLOR,
        validators=[RegexValidator("^([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|)$",
                                   "Color must be 3 or 6-digit hexecimal "
                                   "number, such as FF0000 for red."), ]
    )

    recommendation_tags = models.ManyToManyField(RecommendationTag,
                                                 blank=True)
    currency = models.ForeignKey(Currency, blank=True, null=True,
                                 related_name="startups")
    location_national = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text=("Please specify the country where your main office "
                   "(headquarters) is located")
    )
    location_regional = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text=("Please specify the state, region or province where your "
                   "main office (headquarters) is located (if applicable).")
    )
    location_city = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text=("Please specify the city where your main "
                   "office (headquarters) is located. (e.g. Boston)")
    )
    location_postcode = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text=("Please specify the postal code for your main office "
                   "(headquarters). (ZIP code, Postcode, codigo postal, etc.)")
    )
    date_founded = models.CharField(
        max_length=100,
        blank=True,
        help_text="Month and Year when your startup was founded."
    )
    landing_page = models.CharField(max_length=255, null=True, blank=True)

    @property
    def name(self):
        return self.organization.name

    @property
    def website_url(self):
        return self.organization.website_url

    @property
    def twitter_handle(self):
        return self.organization.twitter_handle

    @property
    def public_inquiry_email(self):
        return self.organization.public_inquiry_email

    class Meta(MCModel.Meta):
        db_table = 'mc_startup'
        managed = is_managed(db_table)
        verbose_name_plural = "Startups"
        ordering = ["organization__name"]

    def __str__(self):
        return self.name
