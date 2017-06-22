# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import (
    datetime,
    timedelta,
)
from pytz import utc

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
    post_generation,
)

from .user_factory import UserFactory
from .program_factory import ProgramFactory


class CoreProfileFactory(DjangoModelFactory):

    class Meta:
        abstract = True

    user = SubFactory(UserFactory)
    privacy_policy_accepted = True
    users_last_activity = utc.localize(datetime.now() + timedelta(-1))
    gender = "p"
    phone = "+1-555-555-5555"
    linked_in_url = Sequence(lambda n: "http://www.linkedin.com/{0}".format(n))
    facebook_url = Sequence(lambda n: "http://www.facebook.com/{0}".format(n))
    twitter_handle = Sequence(lambda n: "tw{0}".format(n))
    personal_website_url = Sequence(
        lambda n: "http://example.com/{0}".format(n))
    landing_page = ""
    image = ""
    drupal_id = 0
    drupal_creation_date = None
    drupal_last_login = None
    current_program = SubFactory(ProgramFactory)
    newsletter_sender = False

    @post_generation
    def recommendation_tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.recommendation_tags.add(tag)

    @post_generation
    def program_families(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.program_families.add(tag)

    @post_generation
    def interest_categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.interest_categories.add(tag)
