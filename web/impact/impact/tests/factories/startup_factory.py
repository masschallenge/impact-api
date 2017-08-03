# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
from pytz import utc
from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
    post_generation,
)

from impact.models import (
    DEFAULT_PROFILE_BACKGROUND_COLOR,
    DEFAULT_PROFILE_TEXT_COLOR,
    STARTUP_COMMUNITIES,
    Startup,
)

from .currency_factory import CurrencyFactory
from .industry_factory import IndustryFactory
from .user_factory import UserFactory
from .organization_factory import OrganizationFactory


class StartupFactory(DjangoModelFactory):
    class Meta:
        model = Startup

    name = Sequence(lambda n: "Test Startup {0} Inc.".format(n))
    organization = SubFactory(OrganizationFactory)
    user = SubFactory(UserFactory)
    is_visible = True
    primary_industry = SubFactory(IndustryFactory)
    short_pitch = "Doing the things with the stuff."
    full_elevator_pitch = "It is really hard to throw elevators."
    video_elevator_pitch_url = "http://example.com"
    website_url = Sequence(lambda n: "startup{0}.com".format(n))
    linked_in_url = Sequence(lambda n: "linkedin.com/startup{0}".format(n))
    facebook_url = Sequence(lambda n: "facebook.com/startup{0}".format(n))
    high_resolution_logo = None
    twitter_handle = Sequence(lambda n: "startup{0}".format(n))
    public_inquiry_email = Sequence(
        lambda n: "contact@startup{0}.com".format(n))
    created_datetime = utc.localize(datetime(2015, 1, 1))
    last_updated_datetime = utc.localize(datetime(2015, 7, 1))
    community = STARTUP_COMMUNITIES[0][0]
    profile_background_color = DEFAULT_PROFILE_BACKGROUND_COLOR
    profile_text_color = DEFAULT_PROFILE_TEXT_COLOR
    currency = SubFactory(CurrencyFactory)
    location_national = "United States"
    location_regional = "Massachusetts"
    location_city = "Boston"
    location_postcode = "02210"
    date_founded = "01/2010"
    landing_page = None

    @post_generation
    def additional_industry_categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for industry in extracted:
                self.additional_industry_categories.add(industry)

    @post_generation
    def recommendation_tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.recommendation_tags.add(tag)
