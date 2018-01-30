# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory,
)
from accelerator.models import SiteProgramAuthorization
from .program_factory import ProgramFactory
from .site_factory import SiteFactory


class SiteProgramAuthorizationFactory(DjangoModelFactory):

    class Meta:
        model = SiteProgramAuthorization

    site = SubFactory(SiteFactory)
    program = SubFactory(ProgramFactory)
    startup_profile_base_url = "http://accelerate.masschallenge.org/finalists/"
    sponsor_profile_base_url = Sequence(
        lambda n: "www.sponsor{0}.com".format(n))
    video_base_url = Sequence(lambda n: "www.video{0}.com".format(n))
    startup_list = False
    startup_profiles = False
    startup_team_members = False
    mentor_list = False
    videos = False
    sponsor_list = False
    sponsor_profiles = False
    sponsor_logos = False
    jobs = False
