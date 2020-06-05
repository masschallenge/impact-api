from rest_framework import serializers

from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import (
    Location,
    MentorProgramOfficeHour,
    User,
    UserRole
)

INVALID_END_DATE = 'office hour end time must be later than the start time'
INVALID_USER = ('must be of type Mentor or Alumni in residence '
                'in an active program')


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

    def validate_mentor(self, mentor):
        user = self.context['request'].user
        if not is_employee(user):
            return user
        roles = [UserRole.MENTOR, UserRole.AIR]
        is_allowed_mentor = mentor.programrolegrant_set.filter(
            program_role__user_role__name__in=roles,
            program_role__program__program_status='active',
        ).exists()
        if not is_allowed_mentor:
            raise serializers.ValidationError(INVALID_USER)
        return mentor

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['mentor'] = UserSerializer(instance.mentor).data
        data['location'] = LocationSerializer(instance.location).data
        return data
