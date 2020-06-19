from datetime import timedelta

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
INVALID_SESSION_TIME = 'Please specify a duration of 30 minutes or more.'
MISSING_START_DATE = "Please specify a start date/time"
MISSING_END_DATE = "Please specify an end date/time"
THIRTY_MINUTES = timedelta(minutes=30)
class OfficeHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProgramOfficeHour
        fields = [
            'id', 'mentor', 'start_date_time', 'end_date_time',
            'topics', 'description', 'location',
        ]

    def validate(self, attrs):
        start_date_time = attrs.get('start_date_time', None)
        end_date_time = attrs.get('end_date_time', None)
        if not start_date_time and not self.instance:
            raise serializers.ValidationError({
                'start_date_time': MISSING_START_DATE})
        if not end_date_time and not self.instance:
            raise serializers.ValidationError({
                'end_date_time': MISSING_END_DATE})
        if start_date_time and end_date_time:
            if start_date_time > end_date_time:
                raise serializers.ValidationError({
                    'end_date_time': INVALID_END_DATE})
            if end_date_time - start_date_time < THIRTY_MINUTES:
                raise serializers.ValidationError({
                    'end_date_time': INVALID_SESSION_DURATION})
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
