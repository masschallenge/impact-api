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
from accelerator.tests.factories.currency_factory import (
    CurrencyFactory as NewCurrencyFactory
)
from .currency_factory import CurrencyFactory as OldCurrencyFactory
from .industry_factory import IndustryFactory
from .user_factory import UserFactory
from .organization_factory import OrganizationFactory


class StartupFactory(DjangoModelFactory):
    class Meta:
        model = Startup

    organization = SubFactory(OrganizationFactory)
    user = SubFactory(UserFactory)
    is_visible = True
    primary_industry = SubFactory(IndustryFactory)
    short_pitch = "Doing the things with the stuff."
    full_elevator_pitch = "It is really hard to throw elevators."
    video_elevator_pitch_url = "http://example.com"
    linked_in_url = Sequence(lambda n: "linkedin.com/startup{0}".format(n))
    facebook_url = Sequence(lambda n: "facebook.com/startup{0}".format(n))
    high_resolution_logo = None
    created_datetime = utc.localize(datetime(2015, 1, 1))
    last_updated_datetime = utc.localize(datetime(2015, 7, 1))
    community = STARTUP_COMMUNITIES[0][0]
    profile_background_color = DEFAULT_PROFILE_BACKGROUND_COLOR
    profile_text_color = DEFAULT_PROFILE_TEXT_COLOR
    currency = SubFactory(OldCurrencyFactory)
    new_currency = SubFactory(NewCurrencyFactory)
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
