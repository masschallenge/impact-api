from graphene_django import DjangoObjectType


from mc.models import Location


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
            'id'
        )
