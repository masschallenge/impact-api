from rest_framework import serializers

from accelerator.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'street_address', 'timezone', 'country',
                  'state', 'name', 'city', ]
