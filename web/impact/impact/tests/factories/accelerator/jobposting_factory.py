# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from factory import DjangoModelFactory
from accelerator.models import JobPosting


class JobPostingFactory(DjangoModelFactory):

    class Meta:
        model = JobPosting
