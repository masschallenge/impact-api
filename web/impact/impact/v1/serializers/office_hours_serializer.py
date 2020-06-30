from datetime import timedelta

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)

from .location_serializer import LocationSerializer
from .user_serializer import UserSerializer
from accelerator_abstract.models.base_clearance import CLEARANCE_LEVEL_STAFF
from accelerator_abstract.models.base_user_utils import is_employee
from mc.utils import swapper_model
MentorProgramOfficeHour = swapper_model("MentorProgramOfficeHour")
UserRole = swapper_model("UserRole")


INVALID_END_DATE = 'office hour end time must be later than the start time'
INVALID_USER = ('must have clearance or be of type Mentor or Alumni in '
                'residence in an active program')
INVALID_SESSION_DURATION = 'Please specify a duration of 30 minutes or more.'
THIRTY_MINUTES = timedelta(minutes=30)
NO_START_DATE_TIME = "start_date_time must be specified"
NO_END_DATE_TIME = "end_date_time must be specified"


class OfficeHourSerializer(ModelSerializer):
    class Meta:
        model = MentorProgramOfficeHour
        fields = [
            'id', 'mentor', 'start_date_time', 'end_date_time',
            'topics', 'description', 'location',
        ]

    def validate(self, attrs):
        start_date_time = None
        end_date_time = None
        if self.instance is not None:
            start_date_time = self.instance.start_date_time
            end_date_time = self.instance.end_date_time

        start_date_time = attrs.get('start_date_time') or start_date_time
        end_date_time = attrs.get('end_date_time') or end_date_time
        if not start_date_time:
            raise ValidationError({
                'start_date_time': NO_START_DATE_TIME})
        if not end_date_time:
            raise ValidationError({
                'end_date_time': NO_END_DATE_TIME})

        if start_date_time > end_date_time:
            raise ValidationError({
                'end_date_time': INVALID_END_DATE})
        if end_date_time - start_date_time < THIRTY_MINUTES:
            raise ValidationError({
                'end_date_time': INVALID_SESSION_DURATION})

        return attrs

    def is_allowed_mentor(self, mentor):
        user = self.context['request'].user
        roles = [UserRole.MENTOR, UserRole.AIR]
        if user == mentor:
            return user.clearances.filter(
                level=CLEARANCE_LEVEL_STAFF,
                program_family__programs__program_status='active'
            ).exists()
        return mentor.programrolegrant_set.filter(
            program_role__user_role__name__in=roles,
            program_role__program__program_status='active',
        ).exists()

    def validate_mentor(self, mentor):
        user = self.context['request'].user
        if not is_employee(user):
            return user
        if not self.is_allowed_mentor(mentor):
            raise ValidationError(INVALID_USER)
        return mentor

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['mentor'] = UserSerializer(instance.mentor).data
        data['location'] = LocationSerializer(instance.location).data
        return data
