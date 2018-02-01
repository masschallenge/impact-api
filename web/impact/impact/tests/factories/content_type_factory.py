# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.contenttypes.models import ContentType
from factory import (
    DjangoModelFactory,
    Sequence,
)


class ContentTypeFactory(DjangoModelFactory):

    class Meta:
        model = ContentType

    # name = Sequence(lambda n: "test_contenttype{0}".format(n))
    app_label = 'accelerator'
    model = Sequence(lambda n: "test_contenttypemodel{0}".format(n))
