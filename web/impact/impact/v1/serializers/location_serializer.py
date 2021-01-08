from rest_framework import serializers

from mc.utils import swapper_model
from mc.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'street_address', 'timezone', 'country',
                  'state', 'name', 'city', ]
