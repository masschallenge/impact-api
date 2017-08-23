from factory import (
    DjangoModelFactory,
    Sequence,
)
from impact.models import Organization


class OrganizationFactory(DjangoModelFactory):

    class Meta:
        model = Organization

    name = Sequence(lambda n: "Test Organization {0}".format(n))
    website_url = Sequence(lambda n: "www.organization{0}.com".format(n))
    twitter_handle = Sequence(lambda n: "organization{0}".format(n))
    public_inquiry_email = Sequence(
        lambda n: "contact@organization{0}.com".format(n))
    url_slug = Sequence(lambda n: "slug{0}".format(n))
