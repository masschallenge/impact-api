from rest_framework import serializers

from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import (
    MentorProgramOfficeHour,
    UserRole
)
from .location_serializer import LocationSerializer
from .user_serializer import UserSerializer

INVALID_END_DATE = 'office hour end time must be later than the start time'
INVALID_USER = ('must be of type Mentor or Alumni in residence '
                'in an active program')


class OfficeHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProgramOfficeHour
        fields = [
            'id', 'mentor', 'start_date_time', 'end_date_time',
            'topics', 'description', 'location',
        ]

    def validate(self, attrs):
        start_datetime = attrs.get('start_date_time', None)
        end_datetime = attrs.get('end_date_time', None)
        if start_datetime and end_datetime and start_datetime > end_datetime:
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
