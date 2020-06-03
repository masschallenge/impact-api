from rest_framework import serializers

from accelerator.models import (
    Location,
    MentorProgramOfficeHour,
    User
)

INVALID_END_DATE = 'office hour end time must be later than the start time'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'street_address', 'timezone', 'country',
                  'state', 'name', 'city', ]


class OfficeHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProgramOfficeHour
        fields = [
            'id', 'mentor', 'start_date_time', 'end_date_time',
            'topics', 'description', 'location',
        ]

    def validate(self, attrs):
        if attrs['start_date_time'] > attrs['end_date_time']:
            raise serializers.ValidationError({
                'end_date_time': INVALID_END_DATE,
            })
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['mentor'] = UserSerializer(instance.mentor).data
        data['location'] = LocationSerializer(instance.location).data
        return data
