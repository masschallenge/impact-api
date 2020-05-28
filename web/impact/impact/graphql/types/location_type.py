from graphene_django import DjangoObjectType


from accelerator.models import Location


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        only_fields = (
            'street_address',
            'timezone',
            'country',
            'state',
            'name',
            'city',
        )
